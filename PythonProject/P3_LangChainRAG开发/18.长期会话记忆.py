import os
import json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory


# message_from_dict: dict -> BaseMessage类实例 [字典,字典...] -> [BaseMessage类实例,BaseMessage类实例...]
# AIMessage\ HumanMessage \ SystemMessage 都是BaseMessage的子类

# 创建一个类继承BaseChatMessageHistory
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id # 会话id
        self.storage_path = storage_path # 不同会话id的存储文件,所在的文件夹路径
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, f"{self.session_id}.json",)

        # 确保文件夹是存在的\
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # 将传入的messages,添加到存储文件里
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list, tuple
        all_messages = list(self.messages) # 已有的消息列表
        all_messages.extend(messages)  # 新的和已有的消息列表进行拼接

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便, 可以将BaseMessage类实例转换成字典(借助json模块以jsoon字符串写入文件)
        # message_to_dict: 单个消息对象(BaseMessage类实例) -> dict

        # new_message = []
        # for message in all_messages:
        #     new_message.append(message_to_dict(message))
        new_message = [message_to_dict(message) for message in all_messages]

        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            '''
            # 1. 先把数据转成 JSON 字符串
            json_str = json.dumps(new_message)
            # 2. 再把字符串写入文件
            with open(self.file_path, "w") as f:
                f.write(json_str)
            而 json.dump(new_message, f) 相当于把这两步合并成了一步，更简洁高效，而且：
            不需要手动创建中间字符串变量
            对大文件更友好（不需要一次性把整个 JSON 字符串加载到内存里）
            '''
            json.dump(new_message, f,ensure_ascii=False)

    # 获取所有消息
    #定义一个叫 messages 的方法
    #返回值类型 必须是：一个列表，列表里每个元素都是 BaseMessage 类型
    @property # @ property装饰器将message方法变成成员属性
    def messages(self) -> list[BaseMessage]:
        # 当前文件内: list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f) # 返回值就是一个列表，列表里每个元素都是 字典
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    # 删除所有消息
    def clear(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump([], f , ensure_ascii=False)



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

def get_history(session_id):
    return FileChatMessageHistory(session_id,"./data") # 创建一个会话历史记录管理器


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
            "session_id": "Text01"
        }
    }
    # res = conversation_chat.invoke({"input": "小明有2只猫"},session_config)
    # print("第一次执行:",res)
    # res = conversation_chat.invoke({"input": "小明有3只狗"},session_config)
    # print("第二次执行:",res)
    res = conversation_chat.invoke({"input": "总共有几只猫"},session_config)
    print("第三次执行:",res)