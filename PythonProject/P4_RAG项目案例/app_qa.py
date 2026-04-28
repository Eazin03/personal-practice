import time
from rag import RagService
import streamlit as st
import config_data as config

# 标题
st.title("智能客服")
st.divider()# 分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "欢迎来到智能客服，请输入您的问题。"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入框
prompt = st.chat_input()

if prompt:

    # 在野蛮输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("正在处理中..."):
        # res = st.session_state.rag.chain.invoke({"input": prompt},config.session_config)
        # st.chat_message("assistant").write(res)
        # st.session_state["message"].append({"role": "assistant", "content":res})

        # 流式输出
        res_stream = st.session_state.rag.chain.stream({"input": prompt},config.session_config)
        # yield迭代器: 每次迭代都会返回一个值,将流式输出的值原封不动返回给用户
        def res_stream_yield(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write(res_stream_yield(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content":"".join(ai_res_list)})
