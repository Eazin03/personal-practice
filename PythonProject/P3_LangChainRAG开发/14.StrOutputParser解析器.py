from langchain_core.output_parsers import  StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage


parser = StrOutputParser()#创建一个StrOutputParser对象
prompt = PromptTemplate.from_template("请将{text}翻译成英文")
model = ChatTongyi(model="qwen3-max")

# chain = prompt | model | parser | model # parser的作用是将前面输出的AIMessage转换成Str类型,继续传入后面的model中
# output: AIMessage = chain.invoke({"text":"你好"})
# print(output.content)

chain = prompt | model | parser | model | parser # parser的作用是将前面输出的AIMessage转换成Str类型,继续传入后面的model中
output: str = chain.invoke({"text":"你好"})
print(output)
print(type(output))# TextAccessor 类是 str 类的一个子类