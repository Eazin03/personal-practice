from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate,ChatPromptTemplate

"""
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
"""
# 创建一个提示词模版
template = PromptTemplate.from_template("我的邻居姓{lastname}, 刚刚生了一个{gender}, 你帮我起一个名字,简单回答。")

# 调用format方法注入信息
format_res = template.format(lastname="张", gender="女儿")
print( format_res,type(format_res))

# 调用invoke方法
invoke_res = template.invoke(input={"lastname": "张", "gender": "女儿"})
print( invoke_res,type(invoke_res))

