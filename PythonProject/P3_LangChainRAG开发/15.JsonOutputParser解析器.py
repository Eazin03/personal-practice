from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  JsonOutputParser,StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi

# 创建所需的解析器: JsonOutputParser,StrOutputParser
json_parser = JsonOutputParser()# 创建一个JsonOutputParser对象,用来解析AI输出的JSON格式数据
str_parser = StrOutputParser()

# 模型创建
model = ChatTongyi(model="qwen3-max")

# 创建第一个提示词模版
first_prompt = PromptTemplate.from_template(
    "我的邻居姓: {lastname}, 刚生了一个{gender}, 请帮忙起一个名字,并封装为JSON格式。"
    "要求key为name,value就是你起的名字,请严格遵守格式要求."
)

# 创建第二个提示词模版
second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 请帮我解析含义.简单回答"
)

# 创造一个链
chain = first_prompt | model | json_parser | second_prompt | model | str_parser
# outPut = chain.invoke({"lastname":"张","gender":"男"})
# print(outPut)
outPut = chain.stream({"lastname":"张","gender":"男"})
for chunk in outPut:
    print(chunk,end="",flush=True)