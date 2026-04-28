from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
'''
PromptTemplate:
模板只写一次，到处用
格式永远统一，AI 输出更稳定
代码超级干净
复杂提示词（RAG、角色设定、多步骤）管理更轻松

'''
# 创建一个提示词模版 --->zero-shot
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚刚生了一个{gender}, 你帮我起个名字,简单回答。"
)

## 标准写法
# # 调用.format方法注入信息即可
# prompt_text = prompt_template.format(lastname="张", gender="女儿")
#
# # 调用tongyi模型
# model  = Tongyi(model="qwen-max")
#
# # 调用invoke方法
# res = model.invoke(input=prompt_text)
# print( res)

# chain链写法
model = Tongyi(model="qwen-max")

chain  = prompt_template | model # 创建一个链,将组件串联,上一个组件的输出作为下一个组件的输入
res = chain.invoke(input = {"lastname": "张", "gender": "女儿"})
print( res)
print(type(res))
