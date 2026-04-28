from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="获取天气信息") # 工具描述:
def get_weather() -> str:
    return "明天是晴天"

agent = create_agent(
    model = ChatTongyi(model="qwen3-max"), # 模型创建
    tools=[get_weather], # 工具列表
    system_prompt= "你是一个聊天助手, 可以回答用户问题" # 系统提示词
)

res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "明天深圳的天气如何?"}
        ]
    }
)

for msg in res["messages"]:
    print(type(msg).__name__,msg.content)
