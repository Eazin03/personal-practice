"""
提示词: 用户的提问 + 向量库中检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings # 将文本转换成向量
from langchain_community.vectorstores import InMemoryVectorStore # 内存向量存储
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "请根据参考资料回答用户问题.参考资料:{context}"),
        ("human", "用户提问:{input}, 请回答用户所问的问题"),
    ]
)

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4"),
)

# 准备一下资料(向量库的数据)
# add_texts 传入一个 list  [str]
vector_store.add_texts(["我叫小王, 喜欢吃苹果", "我叫小张, 喜欢吃香蕉", "我叫小王, 喜欢吃凤梨", "我叫小张, 喜欢吃橘子"])

input_text = "小张喜欢吃什么?"

# 检索向量库
result = vector_store.similarity_search(
    input_text,
    k=2,
)
print(result)
reference_text = "["
for doc in result:
    reference_text += doc.page_content + ";" # 将参考资料拼接成字符串,.page_content表示文档内容
reference_text += "]"
print(reference_text)

# 将链中的数据提取出来
def print_prompt(inputs):
    print("="*20,inputs.to_string(),"="*20)
    return  inputs

# 构建一个链
chain = prompt | print_prompt | model | StrOutputParser()
res = chain.invoke({"input": input_text, "context": reference_text})
print(res)