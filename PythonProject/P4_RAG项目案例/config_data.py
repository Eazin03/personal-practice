md5_path = "./md5.txt"

# Chroma
chroma_db_path = "./chroma_db"
chroma_collection_name = "rag"

# spliter
chunk_size = 1000
chunk_overlap = 100
spliter_separators = ["\n\n", "\n", " ", "", "。", "？", "！", ".", "!", "?"]
max_split_char_number = 1000 # 文本分割的阈值

#
similarity_threshold = 2 # 检索返回匹配的文档数量

embedding_model = "text-embedding-v4"
chat_model = "qwen3-max"

# session_id的配置
session_config = {
    "configurable": {
        "session_id": "Text01"
    }
}