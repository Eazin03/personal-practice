from arrow import now
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
import config_data as config
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import  ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history

def print_prompt(inputs):
    print("=" * 20, inputs.to_string(), "=" * 20)
    return inputs

class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(DashScopeEmbeddings(model=config.embedding_model))

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为参考,请简洁专业的回答用户问题.参考资料:{context}"),
                ("assistant","已获取到与用户沟通的历史记录:"),
                MessagesPlaceholder("history"),
                ("human", "请回答用户问题:{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model)

        self.chain = self._get_chain()

    @staticmethod  # 加 @staticmethod 装饰器（留在类里）如果你一定要放在类里，必须加静态方法装饰器
    def format_func(docs: list[Document]):
        if not docs:
            return "无相关参考资料,自行编写"
        formatted_str = "["
        for doc in docs:
            formatted_str += doc.page_content + " ;"
        formatted_str += "]"
        return formatted_str



    def _get_chain(self): # _表示私有方法，外部不能调用
        # 获取最终地执行链
        retriever = self.vector_store.get_retriever()

        # 定义一个函数: 将输入的input转换成格式
        def format_for_retriever(value):
            return value["input"]

        # 定义一个函数: 将输入的字典转换成格式
        def format_for_prompt(value):
            now_value = {}
            now_value["input"] = value["input"]["input"]
            now_value["context"] = value["context"]
            now_value["history"] = value["input"]["history"]
            return now_value

        chain = (
            {"input": RunnablePassthrough(), "context": RunnableLambda(format_for_retriever) | retriever | self.format_func} | RunnableLambda(format_for_prompt) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversion_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input", # 输入的占位符
            history_messages_key="history" # 历史记录的占位符

        )

        return conversion_chain

if __name__ == '__main__':
    # session_id的配置
    session_config = {
        "configurable": {
            "session_id": "Text01"
        }
    }
    rag_service = RagService().chain.invoke({"input": "这类衣服要怎么清洗呢?"},session_config)
    print(rag_service)