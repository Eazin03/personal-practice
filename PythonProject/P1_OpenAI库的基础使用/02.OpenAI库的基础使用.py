from openai import OpenAI

# 1.获取client对象,OpenAI类对象
client = OpenAI(

    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",  # 模型名称
    messages=[
        {"role": "system", "content": "你是一位Python专家"},# 系统角色
        {"role": "assistant","content": "能够简洁快速的给出答案"},# 角色输出的格式类型
        {"role": "user", "content": "请写一个python代码，实现一个函数，输入一个列表，返回列表中元素出现的次数"}# 用户角色
              ]  # 输入内容

)

# 3.处理结果
print(response.choices[0].message.content)