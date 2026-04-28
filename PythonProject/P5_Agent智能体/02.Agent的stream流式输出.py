from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from pygments.lexers import tcl


@tool(description="获得股价, 传入股票名称,返回字符串信息")
def get_price(name: str) ->str:
    return f"股票{name}价格是100"

@tool(description="获得股票信息, 传入股票名称,返回字符串信息")
def get_info(name: str) ->str:
    return f"股票{name}, 是一家A股上市公司, 专注于IT职业教育"


agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_price, get_info],
    system_prompt="你是一个聊天助手, 可以回答用户问题, 记住请告知我思考过程, 让我知道你为什么调用某个工具"
)

res = agent.stream(
    {
        "messages": [{"role": "user", "content": "传智教育股价多少, 并介绍一下?"}]
    },
    stream_mode="values" # 每步返回完整状态，方便你看到 Agent 的 “全局近况”

)
"""
stream_mode	流的粒度	输出特点	你的体验
values	按节点 / 状态快照	每次返回完整的 state 字典	节点跑完才一次性出内容
updates	按节点更新	每次返回「哪个节点更新了什么」	同样看不到逐字效果
messages	按 token / 消息块	把模型生成的每个 chunk 单独吐出	打字机效果，一个字一个字蹦出来
"""
for chunk in res:
    latest_message = chunk["messages"][-1]

    print(type(latest_message).__name__, latest_message.content)

    try:
        if latest_message.tool_calls:
            print(f"调用工具: {[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError:
        pass


