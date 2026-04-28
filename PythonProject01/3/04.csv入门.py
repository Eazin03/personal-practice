# csv操作 - 方式一:文件操作的原始方式
# 写
# with open("./csv_data/test.csv", "w", encoding="utf-8") as f:
#     f.write("name,age,sex,爱好\n")
#     f.write("小王,18,男,'football,python'\n")
#     f.write("小张,18,男\n")
#     f.write("小李,18,男\n")
#
# # 读
# with open("./csv_data/test.csv", "r", encoding="utf-8") as f:
#     for line in f:
#         print(line.strip())


# csv操作 - 方式二:csv模块
import csv
"""
DictWriter: 表示字典写入csv文件的对象
DictReader: 表示字典读取csv文件的对象
"""
# 写
# newline: 表示写入的行末是否添加换行符
with open("./csv_data/test01.csv", "w", encoding="utf-8", newline="") as f:
    #fieldnames 是表示字段名称的列表
    writer = csv.DictWriter(f,fieldnames=["name","age","sex","hobby"])
    writer.writeheader()#写表头
    writer.writerow({"name":"小王","age":18,"sex":"男","hobby":"football,python"})
    writer.writerow({"name":"小张","age":18,"sex":"男","hobby":"football"})
    writer.writerow({"name":"小李","age":18,"sex":"男","hobby":"python"})
    writer.writerow({"name":"小王","age":18,"sex":"男","hobby":"football,python"})

# 读
with open("./csv_data/test01.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for line in reader:
        print(line)