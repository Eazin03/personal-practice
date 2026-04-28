import json

# 创建一字典对象
dict_obj = {
    "name": "张三",
    "age": 18,
    "gender": "男",
    "hobbies": ["reading", "swimming", "coding"]
}

'''
函数	作用	输出	最常用场景
json.dumps()	转字符串	把 Python 对象 → JSON 格式字符串	网络传输、打印、拼接
json.dump()	写文件	把 Python 对象 → 直接写入文件	保存到本地 .json 文件
'''

# python对象转为json字符串
json_str = json.dumps(dict_obj, ensure_ascii=False) # 设置ensure_ascii=False，可以输出中文
# 直接打印字典和转换为json字符串,区别为json字符串输出的格式不同
print(json_str)

# 反向转换为python对象
json_contrary_str = '{"name": "张三", "age": 18, "gender": "男", "hobbies": ["reading", "swimming", "coding"]}'

res_dict = json.loads(json_contrary_str)
print(res_dict, type(res_dict))