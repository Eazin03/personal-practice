from itertools import chain

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

# 创建所需的解析器: StrOutputParser
str_parser = StrOutputParser()

# 模型创建
model = ChatTongyi(model="qwen3-max")

# 创建第一个提示词模版
first_prompt = PromptTemplate.from_template(
    "我的邻居姓: {lastname}, 刚生了一个{gender}, 请帮忙起一个名字,仅告知名字,不要额外的信息."
)

# 创建第二个提示词模版
second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 请帮我解析含义.简单回答"
)


# 方法一:
# # 自定义函数:函数的入参: AIMessage -> dict ({"name" : "xxx"})
# my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content} )
#
# chain = first_prompt | model | my_func | second_prompt | model | str_parser
# outPut = chain.invoke({"lastname":"张","gender":"男"})
# print(outPut)

# 方法二: 可以直接将自定义函数作为RunnableLambda的参数
chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser
outPut = chain.invoke({"lastname":"李","gender":"女"})
print(outPut)