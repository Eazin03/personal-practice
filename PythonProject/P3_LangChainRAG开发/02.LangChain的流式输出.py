# # langchain_community
# from langchain_community.llms.tongyi import Tongyi
#
# # # 设置API密钥（也可以直接传入api_key参数）
# # os.environ["DEEPSEEK_API_KEY"] = "你的API Key"
#
# # 不用请问-max,因为qwen3-max是聊天模型,qwen-max是大模型语言
# model = Tongyi(model="qwen-max")
#
# # 通过stream方法获得流式输出
# res = model.stream(input="你是谁啊")
#
# for chunk in res:
#     print(chunk, end="", flush=True)

from langchain_ollama import OllamaLLM
from urllib3.contrib.emscripten import response

model = OllamaLLM(model="qwen3:4b")

response = model.stream(input="你是谁啊")

for chunk in response:
    print(chunk, end="", flush=True)