# 读文件
# 1.打开文件
# f = open("resources/望庐山瀑布.txt", "r", encoding="utf-8")
#
# # 2.读取文件内容
# # content = f.read()# 读取所有内容
# # print(content)
#
# content_list = f.readlines()
# print(content_list)
# for line in content_list:
#     print(line.strip())# strip()是用来去掉字符串中的回车换行符
#
# # 3.关闭文件
# f.close()


# 写文件
# # 1.打开文件
# f = open("resources/静夜思.txt", "w", encoding="utf-8")
#
# # 2.写入文件内容
# f.write("静夜思(李白)\n")
# f.write("窗前明月光,\n")
# f.write("疑是地上霜.\n")
# f.write("举头望明月,\n")
# f.write("低头思故乡.")
#
#
#
# # 3.关闭文件
# f.close()

# =============释放资源 方式1================
# # 1.打开文件
# f = open("resources/静夜思.txt", "w", encoding="utf-8")
#
# try:
#     # 2.写入文件内容
#     f.write("静夜思(李白)\n")
#     f.write("窗前明月光,\n")
#     1/0
#     f.write("疑是地上霜.\n")
#     f.write("举头望明月,\n")
#     f.write("低头思故乡.")
# finally:
#     # 3.关闭文件
#     f.close()
#     print("执行成功!")


# =============释放资源 方式2(最佳实践)================
# 1.打开文件
with open("resources/静夜思.txt", "w", encoding="utf-8") as f:
    # 2.写入文件内容
    f.write("静夜思(李白)\n")
    f.write("窗前明月光,\n")
    1/0
    f.write("疑是地上霜.\n")
    f.write("举头望明月,\n")
    f.write("低头思故乡.")