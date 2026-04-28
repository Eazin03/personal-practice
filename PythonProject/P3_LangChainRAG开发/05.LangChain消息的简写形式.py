from langchain_community.chat_models.tongyi import ChatTongyi

from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

model = ChatTongyi(model="qwen3-max")

# 消息内容简写
messages = [
    # (角色,内容),角色: system,human,ai/system,user, assistant
    ("system", "你是一个边塞诗人,能快速输出一首故事"),
    ("human", "写一首唐诗"),
    ("ai", "锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦。"),
    ("human", "按照你上一个回复的格式,再写一首唐诗")
    # SystemMessage(content="你是一个边塞诗人,能快速输出一首故事"),  # 系统消息,相当于OpenAI中的system角色
    # HumanMessage(content="写一首唐诗"),  # 用户消息,相当于OpenAI中的user角色
    # AIMessage(content="锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦。"),  # 模型回复,相当于OpenAI中的assistant角色
    # HumanMessage(content="按照你上一个回复的格式,再写一首唐诗")
]

# 调用stream流式输出,通过.content来获取结果,可以转换为字符串形式输出
for chunk in model.stream(messages):
    print(chunk.content,end="",flush=True)