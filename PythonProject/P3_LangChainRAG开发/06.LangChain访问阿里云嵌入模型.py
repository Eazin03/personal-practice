# 文本嵌入模型
from langchain_community.embeddings import DashScopeEmbeddings
#DashScopeEmbeddings 就是把文字变成 “懂意思” 的数字向量，用来做智能检索、知识库问答、语义去重，是 RAG 和智能文本系统的基础组件

# 创建模型对象 不传model默认为text-embeddings-v1
model = DashScopeEmbeddings(# model="text-embedding-v1")
)

# 不用invoke stream
# embed_query : 将一个文本转为向量\
print(model.embed_query("你好"))
#embed_documents : 将多个文本转为向量
print(model.embed_documents(["你好", "世界"]))
'''
方法 用途 背后的逻辑
embed_query 用于用户的查询（比如 RAG 里的问题） 会自动给文本加上查询指令前缀，比如："为这个问题生成用于检索的向量：你好"
embed_documents 用于知识库的文档片段 会自动给文本加上文档指令前缀，比如："为这个文档片段生成用于检索的向量：你好"
'''

#
# # ollama嵌入模型
# from langchain_ollama import OllamaEmbeddings
#
# model = OllamaEmbeddings(model="qwen3-embedding:4b")
# # 不用invoke stream
# # embed_query : 将一个文本转为向量\
# print(model.embed_query("你好"))
# #embed_documents : 将多个文本转为向量
# print(model.embed_documents(["你好", "世界"]))