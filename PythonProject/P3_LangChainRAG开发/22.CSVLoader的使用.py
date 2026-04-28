from langchain_community.document_loaders import CSVLoader

# 创建一个CSVLoader对象
loader = CSVLoader(
    file_path='./data/students.csv', # csv文件路径
    csv_args={
        "delimiter":"," ,# 指定分隔符,与csv文件的分隔符一致
        "quotechar": '"', # 指定带有分隔符文本的引号包围的是单引号还是双引号
        # 指定csv文件的字段名称,如果数据源没有字段名称,则需要指定字段名称
        "fieldname": ["name", "age", "gender", "hobby"]
    },
    encoding="utf-8", # 文件编码
)

# 批量加载.load()
# documents = loader.load()
#
# print(documents)
'''
Load方法一次性批量加载(返回list内含Document对象)，如内容过多可能list太大，出现内存溢出问题
lazy_load方法会得到生成器对象，可用for循环依次获取单个Document对象，适用于大文档避免内存存不下。
'''
# 懒加载 .lazy_load()
for doc in loader.lazy_load():
    print(doc)

