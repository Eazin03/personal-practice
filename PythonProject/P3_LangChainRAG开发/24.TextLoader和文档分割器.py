from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 创建一个TextLoader对象
loader = TextLoader("./data/python基础语法.txt", encoding="utf-8")

documents = loader.load() # 输出的只有一个元素[Document]

# 创建一个RecursiveCharacterTextSplitter对象
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 分段的最大字符数
    chunk_overlap=50, # 分段之间允许重叠的字符数
    separators=["\n\n", "\n", " ", "", "。", "？", "！", ".", "!", "?"], # 分割符
    length_function=len # 统计字符的依据函数
)


split_docs = text_splitter.split_documents(documents)
"""
split_text：只切文本，元数据会丢失
split_documents：切完后每一段都带着原文档的来源、页码、文件名等信息
split_text：字符串 → 字符串列表
split_documents：Document 列表 → Document 列表（保留元数据，推荐使用）
"""
print(len( split_docs))
for doc in split_docs:
    print("="*20)
    print(doc)
    print("="*20)

