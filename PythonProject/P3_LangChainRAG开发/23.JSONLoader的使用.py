from langchain_community.document_loaders import  JSONLoader
import jq
from openai.types.conversations import text_content

loader = JSONLoader(
    file_path="./data/stu_json_lines.json", # json文件路径
    # jq_schema=".name", # json对象中要提取的字段

    # jq_schema="."是默认值,表示提取整个json对象.同时要把text_content设置为False
    # jq_schema=".",
    # text_content=False, # 告知JSONLoader 我们需要提取的json对象是一个文本内容,而不是一个json对象

    # # jq_schema=".[].name" 表示在json的数组中,提取name字段
    # jq_schema=".[].name"

    jq_schema=".name",
    text_content=False,
    json_lines=True, # 告知JSONLoader 文件格式是JSONLines文件(每一行都是一个json对象)


)

document = loader.load()
print( document)