"""
用于实现向量存储的核心类
"""
from langchain_chroma import Chroma
import config_data as config

class VectorStoreService( object):
    def __init__(self,embedding):
        # :param embedding: 嵌入模型的传入
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.chroma_collection_name,
            embedding_function=self.embedding,
            persist_directory=config.chroma_db_path
        )

    def get_retriever(self):
        # 返回向量检索器, 方便加入chain
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    data = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()

    res = data.invoke("180身高,适合什么尺寸呢")
    print(res)
