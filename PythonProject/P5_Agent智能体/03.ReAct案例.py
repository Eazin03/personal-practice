"""
Agent ReAct 是大模型智能体的核心思考与行动框架，全称 Reasoning+Acting (推理 + 行动), 是让 Agent 像人
类一样「思考问题→制定策略→执行行动→验证结果」的关键逻辑。
简单来说：ReAct 让 Agent 不再是 "直接回答问题", 而是通过 "自然语言思考过程" 指导工具调用，一步步解决复杂问题，
完美适配需要多步推理、工具协作的场景 (如智能客服、报告生成、任务规划等)。

"""


from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from pygments.lexers import tcl


@tool(description="获取体重, 返回值是整数, 单位千克")
def get_weight() ->int:
    return 90

@tool(description="获取身高, 返回值是整数, 单位厘米")
def get_high() ->int:
    return 172


agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weight, get_high],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考一行动观察一再思考」的流程解决问题.
    且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我'"""
)

res = agent.stream(
    {
        "messages": [{"role": "user", "content": "计算一下我的BMI是多少?"}]
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


