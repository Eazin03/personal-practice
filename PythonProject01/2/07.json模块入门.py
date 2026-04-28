import json


# 写入json数据文件
# user = {
#     "name": "Elio",
#     "age": 18,
#     "gender": "男",
#     "hobbies": ["football", "basketball"]
# }
# with open("resources/user.json", "w", encoding="utf-8") as f:
#     # ensure_ascii=False, 保存中文;默认是true
#     # indent: 会在输出的json数据中添加缩进
#     json.dump(user, f, ensure_ascii=False,indent=2)

# 读取json数据文件
with open("resources/user.json", "r", encoding="utf-8") as f:
    user = json.load(f)
    print(user)