from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import  StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory # 内存中存储,只是临时存储,刷新之后就不见了

model = ChatTongyi(model="qwen3-max")
# 输入提示词模版
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题.对话历史:{chat_history}, 用户提问:{input}, 请回答用户所问的问题:"
# )
# 使用ChatPromptTemplate创建一个提示词模版
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "请根据会话历史回答用户问题.对话历史:"),
        MessagesPlaceholder("chat_history"),
        ("human", "用户提问:{input}, 请回答用户所问的问题"),
    ]
)

str_parser = StrOutputParser()

# 创建一个会话历史记录管理器
store = {} # key就是session, value就是InMemoryChatMessageHistory对象
#实现通过会话id获取InMemoryChatMessageHistory对象
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory() # 创建一个会话历史记录管理器
    return store[session_id]

'''
你写的 get_history 只是获取容器的函数，真正的 “写数据” 动作，是由 RunnableWithMessageHistory 这个类的内部逻辑帮你完成的，你不需要手动调用 add_user_message。
举个执行过程的例子：
python
运行
# 调用对话链
response = conversation_chain.invoke(
    {"input": "你好"},
    config={"configurable": {"session_id": "123"}}
)
执行时：
先调用 get_history("123")，发现 store 里没有，就创建一个新的 InMemoryChatMessageHistory，存进 store。
此时 history.messages 是空的，所以 chat_history 占位符是空的。
prompt 模板拿到 input="你好" 和空的 chat_history，生成最终 prompt 传给模型。
模型返回回答后，RunnableWithMessageHistory 自动执行：
python
运行
history.add_user_message("你好")
history.add_ai_message(response)
第二次再调用 invoke 时，get_history("123") 拿到的 history 里，就已经有这两条对话了，会自动填充到 chat_history 里。
'''
# 打印链中的输出
def print_prompt(inputs):
    print("="*20,inputs.to_string(),"="*20)
    return  inputs

# 创建一个基础的链
base_chain = prompt | print_prompt| model | str_parser

# 创建一个新的链,并设置历史记录
conversation_chat = RunnableWithMessageHistory(
    base_chain,   # 被增强的原有chain
    get_history, # 通过会话id获取InMemoryChatMessageHistory对象
    input_messages_key="input",  # 表示用户输入在模版中的占位符
    history_messages_key = "chat_history", # 表示历史记录在模版中的占位符

)

if __name__ == '__main__':

    # 固定格式,添加LangChain的配置, 为当前程序配置所需的session_id
    session_config = {
        "configurable": {
            "session_id": "123"
        }
    }
    res = conversation_chat.invoke({"input": "小明有2只猫"},session_config)
    print("第一次执行:",res)
    res = conversation_chat.invoke({"input": "小明有3只狗"},session_config)
    print("第二次执行:",res)
    res = conversation_chat.invoke({"input": "总共有几只宠物"},session_config)
    print("第三次执行:",res)