from cffi import model
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# 创建一个ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人,能快速输出一首故事"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请再来一首唐诗")
    ]
)

# 创建动态数据
history_data = [
    ("human","你来写一首唐诗"),
    ("ai","锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦。"),
    ("human","请再写一首唐诗"),
    ("ai","烽火连天戍鼓催，  孤城落日角声哀。  胡尘未扫征人老， 一夜乡心随雁来。。"),
]

# prompt_template = chat_prompt_template.invoke({"history" : history_data}).to_string()
# print(prompt_template)
#
# model = ChatTongyi(model="qwen3-max")
# res = model.invoke(input=prompt_template)
# print( res.content)

# 用chain链写法
model = ChatTongyi(model="qwen3-max")

# 组成链, 要求每一个组件都是Runnable接口的子类
# chain = prompt_template | model |xxx | xxx  :只要都是Runnable接口的子类,都可以组成链
# 形成的链对象,是一个RunnableSequence对象(Runnable接口子类)
chain = chat_prompt_template | model

#通过链去调用invoke或stream方法
# invoke_res = chain.invoke(input = {"history": history_data})
# print(invoke_res.content)

# 链式调用stream
stream_res = chain.stream(input = {"history": history_data})# 回复消息为AIMessage对象
for chunk in stream_res:
    print(chunk.content,end="",flush=True)

