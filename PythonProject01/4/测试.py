# import pandas as pd
#
# # 构建DataFrame -- 创建数据集(学员成绩信息)
# df = pd.DataFrame([
#     {"姓名": "小王", "性别": "男", "年龄": 18, "成绩": 90},
#     {"姓名": "小张", "性别": "女", "年龄": 18, "成绩": 80},
#     {"姓名": "小李", "性别": "男", "年龄": 18, "成绩": 70},
#     {"姓名": "小王1", "性别": "男", "年龄": 18, "成绩": 60},
#     {"姓名": "小王32", "性别": "男", "年龄": 18, "成绩": 50},
#     {"姓名": "小王3", "性别": "男", "年龄": 18, "成绩": 40},
#     {"姓名": "小王4", "性别": "男", "年龄": 18, "成绩": 30},
#     {"姓名": "小王5", "性别": "男", "年龄": 18, "成绩": 20},
# ])
#
# print(df)

import matplotlib.pyplot as plt
import random

from matplotlib.lines import lineStyles
from traitlets import link

# 展示中文
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体为黑体

# 绘制折线图
x = [i for i in range(1,25)]
y_bj = [random.randint(1,30) for i in x]
y_xa = [random.randint(1,30) for i in x]


plt.figure(figsize=(10,5)) # 设置画布的大小, 宽高比为10:5
# 绘制折线图
plt.plot(x,y_bj, label="北京") # 绘制折线图 ->如果没有画布,则会创建一个画布
plt.plot(x,y_xa, label="西安")

# 设置折线图的详细信息
plt.title("气温变化折线图", fontsize=15)
plt.xlabel("时间", fontsize=10)
plt.ylabel("气温", fontsize=10)
# plt.xticks(x[::2])
# plt.xticks(x[1::2])
plt.xticks(x)
plt.yticks(range(0,31))
plt.grid(linestyle='--', alpha=0.3) #lineStyle: 线的样式, alpha: 透明度
plt.legend(loc ="upper right")

plt.show()#显示折线图