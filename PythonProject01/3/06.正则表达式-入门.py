
# 正则表达式
import re
s1="18809090000 是我的手机号，你记住了吗？我的另一个个手机号是 18800008888, 两个 QQ 号分别是 155998992 和 183809091293821 你记住了吗？"
s2=" 我的手机号是 18809090000, 你记住了吗？我的另一个个手机号是 18800008888, 两个 QQ 号分别是 155998992 和 188809091293821 你记住了吗？"

# match - 从字符串开头匹配(匹配第一个字符串) ---> match对象
# r""是用于表示\就是属于\的,不会进行转义
# pattern = re.match(r"1[3-9]\d{9}", s1)
# # group(): 获取匹配的字符串
# print(pattern.group())
# print(pattern.span())# 获取匹配的索引
# print(pattern.start())# 获取匹配的开始索引
# print(pattern.end())# 获取匹配的结束索引

# search - 从字符串 anywhere 匹配(匹配任意位置的字符串) ---> match对象
# pattern = re.search(r"1[3-9]\d{9}", s2)
# print(pattern.group())


# findall - 匹配所有字符串 ---> 列表
print(re.findall(r"1[3-9]\d{9}", s2))


