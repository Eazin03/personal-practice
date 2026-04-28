"""
它的核心用途（你必须记住这 4 个）
1. 日志 / 监控（最常用）
记录每一步输入、输出
打印状态变化
方便调试 Agent 为什么卡住、为什么调用工具
2. 权限 / 校验
检查用户能不能执行这个节点
检查输入是否合法
拦截危险操作
3. 修改输入 / 输出（拦截器）
自动修改传给节点的参数
自动修改节点返回的结果
不改动原节点代码
4. 统一处理
统一错误捕获
统一加重试
统一加超时

三、生活类比（秒懂）
Agent 流程 = 你去坐飞机
中间件 = 安检、检票、行李扫描
你不用改变 “坐飞机” 这个流程
但流程前后会自动被检查、记录、控制
"""
from textwrap import wrap

from langchain.agents import create_agent,AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime

@tool(description="查询天气, 传入城市名称, 返回字符串信息") # 工具描述:
def get_weather(city: str) -> str:
    return f'{city}天气是晴天'

# agent 执行前
@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    # agent执行前会调用这个函数, 并传入 agent 的状态和运行时对象
    print(f'[before agent]agent启动, 并附带{len(state["messages"])}条消息')



# agent 执行后
@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    # agent执行后会调用这个函数, 并传入 agent 的状态和运行时对象
    print(f'[after agent]agent结束, 并附带{len(state['messages'])}条消息')



# model 执行前
@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f'[before model]model即将调用, 并附带{len(state['messages'])}条消息')


# model 执行后
@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f'[after model]model已调用, 并附带{len(state['messages'])}条消息')



# 工具执行中
@wrap_tool_call
def tool_call_hook(request, handler):
    print(f'工具执行:{request.tool_call["name"]}')
    print(f'工具参数:{request.tool_call["args"]}')
    return handler(request)


# 模型执行中
@wrap_model_call
def model_call_hook(request, handler):
    # 模型执行中会调用这个函数, 并传入 request 和 handler, request 是模型调用的参数, handler 是模型调用的函数
    """
    request是一个字典对象，包含了模型调用时的请求数据，request['messages']是历史消息列表，包含对话上下文；
    handler是一个函数对象，代表实际的模型调用处理函数，接收request作为参数，返回模型的response结果
    """
    print("模型调用啦!")
    return handler(request)

agent = create_agent(
    model = ChatTongyi(model="qwen3-max"), # 模型创建
    tools=[get_weather], # 工具列表
    middleware=[
        log_before_agent,
        log_after_agent,
        log_before_model,
        log_after_model,
        tool_call_hook,
        model_call_hook
    ],# 中间件列表
)

res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "深圳的天气如何?"}
        ]
    }
)

for msg in res["messages"]:
    print(type(msg).__name__,msg.content)
