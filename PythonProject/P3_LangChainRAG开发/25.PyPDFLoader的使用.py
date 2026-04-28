from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/未命名1_加水印.pdf",
    mode="page", # 默认值,表示加载pdf中的每一页,每一个页面形成一个Document对象; single模式,表示加载pdf中的所有内容到一个Document对象中
    password="123456", # 加密pdf的密码
)

i=0
for doc in loader.lazy_load(): # 懒加载,一次加载一个Document对象
    i +=1
    print(doc)
    print( i)