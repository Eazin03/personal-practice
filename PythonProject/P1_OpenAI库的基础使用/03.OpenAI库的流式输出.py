from httpcore import stream
from openai import OpenAI

# 1.获取client对象,OpenAI类对象
client = OpenAI(

    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",  # 模型名称
    messages=[
        {"role": "system", "content": "你是一位Python专家"},# 设定AI的身份和行为准则(回答的风格、限制、规则等)
        {"role": "user", "content": "请写一个python代码，实现一个函数，输入一个1-10数字"}# 用户实际提出的问题或指令
              ],  # 输入内容
    stream= True
)
'''
  先看两个场景的核心区别
  表格
  代码	运行环境	输出方式	核心问题
  第一段	纯 Python 控制台	print() 直接输出	控制台是 “增量追加” 模式，新内容直接接在后面
  第二段	Streamlit Web 页面	st.chat_message().write() 输出	Streamlit 每次 write() 都会重新渲染整个组件，不做处理会重复叠加
  '''
# 3.处理结果
for chunk in response:
    print(chunk.choices[0].delta.content,end= "",flush= True)# 设置flush=True, 可以使输出立即显示,刷新缓存区