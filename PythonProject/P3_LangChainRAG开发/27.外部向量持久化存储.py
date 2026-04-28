# 内存向量存储的核心类
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# Chroma 向量数据库(轻量级的)
from langchain_chroma import Chroma

inMemory = Chroma(
    collection_name= "test", # 当前向量存储起个名字, 类似数据库的表名称
    embedding_function=DashScopeEmbeddings(), # 嵌入模型
    persist_directory="./chroma_db" # 指定数据存放的文件夹
)

# loader = CSVLoader(
#     file_path='./data/info.csv',
#     encoding="utf-8",
#     source_column="source"  # 指定本条数据的来源列
# )
#
# docs = loader.load()
#
#
# # 向量存储的新增 \ 删除 \ 检索
# inMemory.add_documents(
#     documents=docs, # 被添加的文档, 类型: list[Document]
#     ids=["id"+str(i) for i in range(1,len(docs)+1)], # 文档的id, 类型: list[str]
# )
#
# # 删除
# inMemory.delete(["id1","id2"])

# 检索
res = inMemory.similarity_search(
    "Python是不是简单易学呀", # 检索的文本
    k=3, # 检索的结果要几个
    filter={"source": "黑马程序员"} # 指定来源
)

print( res)