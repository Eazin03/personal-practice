"""
知识库
在这个场景里，MD5 主要用来做 **“数据指纹”**，实现两个关键目标：

数据去重，避免重复处理
你给数据 / 文件计算出 MD5 值后，就可以把它当成这个数据的 “唯一标识”
每次处理前，用check_md5查一下：如果这个 MD5 值已经在记录文件里，说明数据已经处理过了，直接跳过；如果没有，就处理数据，处理完用save_md5把 MD5 值存起来
这样就不会对同一份数据重复执行耗时操作（比如爬虫、解析、入库），节省资源

数据完整性校验（延伸用途）
只要数据 / 文件的内容发生哪怕一点点变化，重新计算出的 MD5 值就会和原来不一样
所以它也可以用来验证数据在传输、存储过程中有没有被篡改或损坏，确保数据的一致性
"""
import os

from datetime import datetime
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config
import hashlib # 可以计算字符的md5值
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def check_md5(md5_str: str):
    # 检查传入的md5字符串是否已经被处理过了, 如果已经被处理过了,则返回True
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在, 那肯定没有处理过这个md5字符串
        open(config.md5_path, "w", encoding="utf-8").close()# 创建一个空文件
        return False
    else:
        # if进入表示文件存在, 那么需要判断文件中的内容是否和传入的md5字符串一致
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip() # 去除换行符,处理字符串前后的空格和回车
            if line == md5_str:
                return True  # 表示已经处理过这个md5字符串了,返回True
    return  False


def save_md5(md5_str: str):
    # 将传入的md5字符串,记录到文件内保存
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")

def get_string_md5(input_str: str, encoding="utf-8"):
    # 将传入的字符串转换为md5字符串

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding= encoding)

    # 创建一个md5对象
    md5_obj = hashlib.md5() # 得到md5对象
    md5_obj.update(str_bytes) # 输入字符串的bytes字节数组
    return md5_obj.hexdigest()# 获取md5的16进制字符串


class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件不存在则创建, 如果存在则跳过
        os.makedirs(config.chroma_db_path, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.chroma_collection_name, # 当前向量存储起个名字, 类似数据库的表名称
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"), # 嵌入模型
            persist_directory=config.chroma_db_path, # 数据库本地存储文件夹
        ) # 向量存储的实例 Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, # 分段最大字符数
            chunk_overlap=config.chunk_overlap, # 分段之间允许重叠的字符数
            separators=config.spliter_separators, # 自然段落分割符
            length_function=len # 使用Python的len函数来统计字符数
        ) # 文档分割器的对象

    def uploader_by_str(self,data: str,filename):
        # 将传入的字符串,进行向量化,存入向量数据库中
        # 先得到传入字符串的md5字符串
        md5_str = get_string_md5(data)
        if check_md5(md5_str):
            return "数据已经处理过了,请勿重复处理"

        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        # 错误写法
        # self.chroma.add_texts(
        #     # iterable迭代器，迭代器对象，迭代器对象是一个可以重复迭代的序列对象，比如列表、元组、字典、字符串等等。
        #     knowledge_chunks,
        #     metadatas=[
        #         {"source": filename},
        #         {"create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        #         {"operator": "小熠"}
        #     ],
        #     ids=[filename]
        # )
        """
        Chroma（向量库）有一个铁律：
            文本有多少段，metadatas 就必须有多少个完整字典！
            一段文本 ↔ 一个完整字典（包含所有信息）
        """
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小熠"
        }
        # 内容加载到向量数据库中
        self.chroma.add_texts(
            # iterable迭代器，迭代器对象，迭代器对象是一个可以重复迭代的序列对象，比如列表、元组、字典、字符串等等。
            knowledge_chunks,
            metadatas = [ metadata for _ in knowledge_chunks ],
            ids= [f"{filename}_{i}" for i in range(len(knowledge_chunks))]  # 每一段给一个唯一ID # ids是每个文本的id
        )

        # 保存md5字符串
        save_md5(md5_str)

        return "上传成功! ! !"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.uploader_by_str("你好1", "test")
    print(r)