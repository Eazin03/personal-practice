import streamlit as st
import os
from openai import OpenAI

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",# 可以占据整个页面, centered:居中, none:默认
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 大标题
st.title("AI智能伴侣")

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示聊天信息
for message in st.session_state.messages:
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])
    st.chat_message(message["role"]).write(message["content"])

# 来创建与AI大模型交互的客户端对象( DEEPSEEK_API_KEY 环境变量的名字, 值就是DEEPSEEK的API_KEY)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

# 系统提示词
system_prompt = "你是一个ai助理,能够快速简洁的回答问题"

# 消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:#字符串会自动转换为布尔值,如果输入的字符串不为空,则返回True
    st.chat_message("user").write(prompt) # user是显示的用户名,assistant是显示的ai回复
    print("---------->这是用户输入的prompt:",prompt)
    # 保存用户输入的prompt
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型
    # 与ai大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    # ai回复的内容
    print("<------ ai大模型回复的内容:",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)
    # 保存ai大模型回复的内容
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})