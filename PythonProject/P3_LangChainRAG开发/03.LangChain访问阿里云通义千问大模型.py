# langchain_community
from langchain_community.llms.tongyi import Tongyi

# # 设置API密钥（也可以直接传入api_key参数）
# os.environ["DEEPSEEK_API_KEY"] = "你的API Key"

# 不用请问-max,因为qwen3-max是聊天模型,qwen-max是大模型语言
model = Tongyi(model="qwen-max")

# 调用invoke向模型提问
res = model.invoke(input="你是谁啊")
print( res)