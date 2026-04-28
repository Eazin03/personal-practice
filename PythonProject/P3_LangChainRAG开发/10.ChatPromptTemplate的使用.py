from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# 创建一个ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人,能快速输出一首故事"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请再来一首唐诗")
    ]
)

# 创建动态数据
history_data = [
    ("human","你来写一首唐诗"),
    ("ai","锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦。"),
    ("human","请再写一首唐诗"),
    ("ai","西风瘦马,客输西风。西风瘦马,客输西风。西风瘦马,客输西风。西风瘦马,客输西风。"),
]

# 是用invoke方法将history_data注入到prompt_text
prompt_text = chat_prompt_template.invoke({"history" : history_data}).to_string()
print(prompt_text)
#第 22 行invoke是模板对象调用，传参填充模板生成prompt_text；
# 第 27 行是模型对象model调用，传入prompt_text获取结果，前者是生成提示文本，后者是用提示文本获取模型输出，作用不同。
# 创建模型对象
model = ChatTongyi(model="qwen3-max")
res = model.invoke(input=prompt_text)
# 通过.content来获取结果,可以转换为字符串形式输出
print( res.content)