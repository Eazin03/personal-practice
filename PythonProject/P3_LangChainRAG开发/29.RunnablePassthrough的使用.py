"""
提示词: 用户的提问 + 向量库中检索到的参考资料
"""

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings # 将文本转换成向量
from langchain_community.vectorstores import InMemoryVectorStore # 内存向量存储
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "请根据参考资料回答用户问题.参考资料:{context}"),
        ("human", "用户提问:{input}, 请回答用户所问的问题"),
    ]
)

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v1"),
)

# 准备一下资料(向量库的数据)
# add_texts 传入一个 list  [str]
vector_store.add_texts(["我叫小王, 喜欢吃苹果", "我叫小张, 喜欢吃香蕉", "我叫小王, 喜欢吃凤梨", "我叫小张, 喜欢吃橘子"])

input_text = "小张喜欢吃什么?"

# langchain中向量存储对象, 有一个办法: as_retriever, 可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k":2}) # search_kwargs: 搜索参数



# 构建一个链
'''
用户输入问题：chain.invoke("怎么减肥？")
第一步：拆分输入
input：直接拿到用户的问题 "怎么减肥？"
context：先通过retriever检索到 3 条相关资料，再用format_func拼接成一段文本
第二步：填充 prompt 模板
把context和input填入模板，生成：
plaintext
system: "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:减肥就是要少吃多练。
在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来。跑步是很好的运动哦。"
user: "用户提问: 怎么减肥？"
第三步：调用大模型
把上面的 prompt 发给模型，模型返回回答结果
第四步：解析输出
把模型返回的结果转换成纯文本，作为最终输出
'''

# 自定义格式化函数: 将 Document 对象列表转换成纯文本
def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料,自行编写"
    formatted_str = "["
    for doc in  docs:
        formatted_str += doc.page_content + " ;"
    formatted_str += "]"
    return formatted_str

# 将链中的数据提取出来
def print_prompt(inputs):
    print("="*20,inputs.to_string(),"="*20)
    return  inputs

chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
) # 字典也是可以入链的
"""
1. 最外层：{ "input": RunnablePassthrough(), "context": retriever | format_func }
这是链的输入阶段，负责给后面的prompt准备两个变量：input和context。
"input": RunnablePassthrough()：
RunnablePassthrough() 就是 “直接透传” 的意思，用户输入的问题（比如 “怎么减肥？”）会直接赋值给input变量，原封不动往下传。
"context": retriever | format_func：
这部分负责生成参考资料，分成两步：
retriever：向量库检索器，会拿着用户的问题，去向量库中找出最相关的资料（比如你代码里的 “减肥就是要少吃多练” 等句子）。
format_func：自定义格式化函数，把检索出来的文档列表，拼接成一段通顺的文本（比如用换行或空格连起来），赋值给context变量。
"""
"""
retriever:
    - 输入: 用户的提问 ---> str
    - 输出: 向量库的检索结果 ----> list[Document]
prompt:
    - 输入: 用户的提问 + 向量库的检索结果 --->dict
    - 输出: 完整的提示词 --> PromptValue
"""

res = chain.invoke(input_text)
print(res)
