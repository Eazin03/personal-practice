import os
from typing import Sequence
import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.output_parsers import StrOutputParser


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

# 创建一个会话历史记录管理器

def get_history(session_id):
    return FileChatMessageHistory(session_id,"./data") # 创建一个会话历史记录管理器


