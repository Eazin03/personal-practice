# 导入streamlit
import streamlit as st

# 设置页面的配置项
st.set_page_config(
    page_title="streamlit 入门实战",
    page_icon="🧊",
    layout="wide",# 可以占据整个页面, centered:居中, none:默认
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.baidu.com',
        'Report a bug': "https://www.baidu.com",
        'About': "# 这是一个streamlit的页面测试"
    }
)


# 大标题
st.title("Streamlit 入门演示")
st.header("Streamlit 一级标题")
st.subheader("Streamlit 二级标题")

# 段落文字
st.write("Streamlit 是一个专门为 Python 打造的轻量级 Web 应用框架，它最核心的优势就是让你完全不用接触 HTML、CSS、JavaScript 这些前端技术，只用纯 Python 代码就能快速搭建出交互式的数据看板、可视化工具或者小应用，不管是用来做数据分析的结果展示、机器学习模型的 Demo，还是日常工作里的实用小工具，它都能帮你把想法快速变成可交互的网页界面，整个过程几乎没有学习门槛。")
st.write("它的使用逻辑特别简单，你只需要用 Python 写好数据处理和业务逻辑，再用 Streamlit 自带的 API 调用组件就可以了，从文本标题、数据表格，到各种交互式控件比如按钮、滑块、下拉框、文件上传器，再到 Matplotlib、Plotly 这类常用可视化库的图表，都能直接渲染到网页上，而且它自带实时热重载功能，每次修改代码保存后，浏览器里的界面就会自动刷新，不用手动重启服务或者刷新页面，调试和开发的效率很高。")
st.write("它的底层是基于 Tornado 实现的，运行起来非常轻量，启动速度很快，本地运行的时候只需要一行命令就能启动服务，部署也特别方便，不仅可以一键部署到免费的 Streamlit 社区云平台，也能打包成 Docker 镜像，或者部署到主流的云服务器上，不用复杂的配置流程。它特别适合数据分析师、算法工程师或者 Python 开发者快速搭建原型和展示工具，不用花时间学习前端知识，把更多精力放在业务和数据本身，就能快速做出可用的交互式应用。")


# 图片
st.image("./resources/OIP-C (2).jpg")
st.image("resources/OIP-C (2).jpg")


#音频
st.audio("./resources/杨子杰——个人演讲 - 副本.mp3")

# 视频
st.video("./resources/hero-video.mp4")

# logo
st.logo("./resources/医院logo.png",size="large")

# 表格
student_data = {
    "姓名": ["倪宁","李虎","玉林","巴克利","如懿"],
    "学号": ["20260001", "20260002", "20260003", "20260004", "20260005"],
    "语文": [98, 90, 59, 29, 80],
    "数学": [88, 78, 65, 70, 39],
    "英语": [99, 89, 87, 59, 62],
    "总分": [285, 257, 211, 158, 181]
}
st.table(student_data)
st.dataframe(student_data) # 添加表头样式

# 输入框
# 普通输入框
name = st.text_input("请输入你的姓名")
st.write(f'你的姓名为: {name}')

# 密码输入框
password = st.text_input("请输入你的姓名",type="password")
st.write(f'你的姓名为: {password}')

# 单选按钮
gender = st.radio("请选择你的性别",["男","女","未知"],index = 2)