# 导入prompt模板类
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

# 创建一个提示词模版
prompt_template = PromptTemplate.from_template(
    "单词: {word} , 反义词: {antonym}"
)

# 示例的动态数据注入 要求输入的数据格式为字典
prompt_text = [
    {"word": "大", "antonym": "小"},
    {"word": "高", "antonym": "低"},
]

# 创建一个 few-shot 提示词模版
few_shot_template = FewShotPromptTemplate(
    example_prompt=prompt_template, # 示例数据的模板
    examples=prompt_text, # 示例数据(用来注入动态数据),list内嵌套字典
    prefix="告知我单词的反义词,提供如下的示例", # 提示词的前缀
    suffix="基于前面的示例,简洁的告诉我{input_word}的反义词?", # 提示词的后缀
    input_variables=['input_word'], # 声明在前缀或后缀中需要动态注入的数据
)
# 调用invoke方法
prompt_show = few_shot_template.invoke(input={"input_word": "左"}).to_string()# to_string()方法将prompt转为字符串
print(prompt_show)

# 导入模型
model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_show)
print( res)