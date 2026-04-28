"""
基于Streamlit完成WEB网页上传服务

Streamlit: 当WEB页面元素发生变化, 则代码会重新运行一遍
"""

import streamlit as st
import time

from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# file_uploader: 添加文件上次功能
uploader_file = st.file_uploader(
    "请上次TXT文件", # 提示词
    type = ['txt'], # 文件上传所支持的类型
    accept_multiple_files=False, # false表示仅接受一个文件的上传,True可以接受多文件上传

)

# session_state就是一个临时存储空间, 可以保存一些数据, 在页面刷新后, 数据会丢失--->dict
if 'counter' not in st.session_state:
    st.session_state['counter'] = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 # 可以得到KB
    st.subheader(f'文件名为: {file_name}')
    st.write(f'文件类型为: {file_type} | 文件大小为: {file_size:.2f}KB')

    # get_value: 获取上传文件的内容 -->bytes(得到的是字节数组) --> 通过decode()方法转换为字符串
    file_content = uploader_file.getvalue().decode("utf-8")

    with st.spinner("正在处理中..."): # 在spinner内的代码会被执行, 显示一个加载动画
        time.sleep(1)
        response = st.session_state['counter'].uploader_by_str(file_content, file_name)
        st.write(response)