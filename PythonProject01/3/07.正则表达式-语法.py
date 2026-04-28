import re

s1="18809090000 是我的手机号，你记住了吗？我的另一个个手机号是 18800008888, 两个 QQ 号分别是 155998992 和 183809091293821 你记住了吗？12255058642745,这个邮箱是python856@163.com"

# 正则表达式
# print(re.findall(r"188.*",s1)) # * 匹配任何个字符串
# print(re.findall(r"188.?", s1))# ? 匹配任意个字符串,但是最多一个
# print(re.findall(r"188.+", s1))# + 匹配任意个字符串,至少一个

# print(re.findall(r"188\d{8}",s1)) # {8}匹配8个
# print(re.findall(r"155\d{6,10}", s1)) # {6,10} L匹配6到10个
# print(re.findall(r"155\d{6,}", s1)) # {6,}匹配6个或者更多

# print(re.findall(r"1[38]\d{8}", s1))# [38]匹配3或8
# print(re.findall(r"1[^38]\d{8}", s1))# 匹配1开头的除3或8
# print(re.findall(r"1[3-9]\d{8}", s1))# 匹配1开头的3-9
# print(re.findall(r"^1[3-9]\d{9}", s1))# ^匹配开头
# print(re.findall(r"^1[3-9]\d{9}$", s1))# $ 匹配结尾

# print(re.findall(r"\w+@\w+\.\w+", s1)) # \w+ 匹配任意个字母数字其他语言字符或下划线
# print(re.findall(r"\w+@\w+\.\w+", s1, re.ASCII))# ASCII 匹配任意个字母数字或下划线


#注意
# s2 = "现在的时间是 2026-02-0610:05:25, 今天的天气还可以以，气温是 28 度"
# print(re.findall(r"\d{4}-\d{2}-\d{2}", s2))
# print(re.findall(r"(\d{4})-(\d{2})-(\d{2})", s2))

s="1h 5m"
print(re.findall(r"\d+", s))