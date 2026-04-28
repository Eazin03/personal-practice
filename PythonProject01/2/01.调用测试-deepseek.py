# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

# 来创建与AI大模型交互的客户端对象( DEEPSEEK_API_KEY 环境变量的名字, 值就是DEEPSEEK的API_KEY)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

# 与ai大模型进行交互
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个ai助理,能够快速简洁的回答问题"},
        {"role": "user", "content": "你是谁?"},
    ],
    stream=False
)
'''
  先看两个场景的核心区别
  表格
  代码	运行环境	输出方式	核心问题
  第一段	纯 Python 控制台	print() 直接输出	控制台是 “增量追加” 模式，新内容直接接在后面
  第二段	Streamlit Web 页面	st.chat_message().write() 输出	Streamlit 每次 write() 都会重新渲染整个组件，不做处理会重复叠加
  '''
# ai回复的内容
print(response.choices[0].message.content)