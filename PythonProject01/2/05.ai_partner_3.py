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

# 系统提示词
system_prompt = "你叫%s,是%s"


# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小熠"
# 性格
if "personality" not in st.session_state:
    st.session_state.personality = "一个ai助理, 能够快速简洁的回答问题"


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


# 左侧的侧边栏
# st.sidebar.subheader("伴侣信息")
# nick_name = st.sidebar.text_input("请输入你的昵称")
# 使用with后面写在侧边栏的内容, 会自动创建一个侧边栏,同时不用写sidebar
with st.sidebar:
    st.subheader("伴侣信息")
    # 输入昵称
    nick_name = st.text_input("昵称" , placeholder="请输入你的昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    # 输入性格
    personality = st.text_area("性格", placeholder="请输入你的性格",value=st.session_state.personality)
    if personality:
        st.session_state.personality = personality


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
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.personality)},
            #*代表着能快速解包, 即把列表中的元素解包
            *st.session_state.messages
        ],
        stream=True
    )

    # ai回复的内容 (非流式输出方式)
    # print("<------ ai大模型回复的内容:",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    # ai回复的内容 (流式输出方式)
    response_message = st.empty() # 创建一个空的组件, 用于显示ai大模型回复的内容
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    # 保存ai大模型回复的内容
    st.session_state.messages.append({"role": "assistant", "content": full_response})