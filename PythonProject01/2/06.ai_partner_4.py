import streamlit as st
import os
from openai import OpenAI
import datetime
import json

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",# 可以占据整个页面, centered:居中, none:默认
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 生成会话标识
def generate_session_id():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 保存会话信息函数
def save_session_info():
    # 1.保存当前会话信息
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "personality": st.session_state.personality,
            "current_session": st.session_state.current_session,
            "message": st.session_state.messages
        }

        # 如果sessions目录不存在,则创建
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

# 展示会话列表信息
def load_session_info():
    session_list = []
    if os.path.exists("sessions"):
        for file in os.listdir("sessions"):
            if file.endswith(".json"):
                session_list.append(file[:-5])
    return session_list

# 加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.personality = session_data["personality"]
                st.session_state.current_session = session_name
                st.session_state.messages = session_data["message"]
    except Exception as e:
        print(e)
        st.error("会话加载失败! ")


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
# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_id()



# 展示聊天信息
st.text(f'会话标题: {st.session_state.current_session}')
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
    #会话信息
    st.subheader("AI控制面板")

    # 新建会话按钮
    if st.button("新建会话",width="stretch",icon="✏️"):
        # 保存当前会话信息
        save_session_info()

        # 创建新的会话
        if st.session_state.messages: # 如果有聊天记录, 则创建新的会话
            st.session_state.messages = []
            st.session_state.current_session = generate_session_id()
            save_session_info()
            st.rerun() # 重新运行当前页面

    # 展示会话列表
    st.text("会话历史")
    session_list = load_session_info()
    for session in session_list:
        col1,col2 = st.columns([4,1])# column是用来创建列的, columns是创建多个列的, columns([1,2,3])创建三个列, 1,2,3是列的宽度比例, 1:2:3表示1列占33.3%, 2列占33.3%, 3列占33.3%
        with col1:
            # 加载会话
            # 三元运算符: 如果条件为真, 则返回第一个值, 否则返回第二个值-->语法: 条件?真值:假值
            if st.button(session ,width="stretch",icon="📝",key= f'load_{session}',type= "primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("",width="stretch",key=f'delect_{session}',icon="❌️"):# key是一个唯一的标识符, 用来区分按钮
                pass



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

    # 保存会话信息
    save_session_info()