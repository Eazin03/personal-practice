# 读文件
"""
路径写法:
    相对路径: 从当前文件所在目录开始查找
    .: 当前目录 ---> ./resources/望庐山瀑布.txt  ./可以省略
    ..: 上一级目录 ---> ../resources/望庐山瀑布.txt  ../../1/file/望庐山瀑布.txt
    绝对路径: 从根目录开始查找
    C:/Users/Administrator/Desktop/望庐山瀑布.txt(注意: \ 在Python中是一个特殊字符, 需要用\\转义)
    C:\\Users\\Administrator\\Desktop\\望庐山瀑布.txt 两个方法都可以
"""

# 1.打开文件
with open("./resources/望庐山瀑布.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)


# 写文件
# a: append, 追加内容;w: write, 写入内容;---> 如果文件不存在, 则创建文件;
with open("./resources/静夜思.txt", "a", encoding="utf-8") as f:
    f.write("静夜思(李白)\n")
    f.write("窗前明月光,\n")
    f.write("疑是地上霜.\n")
    f.write("举头望明月,\n")
    f.write("低头思故乡.")