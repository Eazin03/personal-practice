# 调用聊天模型
from langchain_community.chat_models.tongyi import  ChatTongyi
from langchain_core import messages
# langchain_core: 语言核心
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

# 得到模型对象
model = ChatTongyi(model="qwen3-max")

# 准备消息列表
messages = [
    SystemMessage(content="你是一个边塞诗人,能快速输出一首故事"),# 系统消息,相当于OpenAI中的system角色
    HumanMessage(content="写一首唐诗"),# 用户消息,相当于OpenAI中的user角色
    AIMessage(content="锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦。"),# 模型回复,相当于OpenAI中的assistant角色
    HumanMessage(content="按照你上一个回复的格式,再写一首唐诗")
]

# 调用stream流式输出,通过.content来获取结果
for chunk in model.stream(messages):
    print(chunk.content,end="",flush=True)
