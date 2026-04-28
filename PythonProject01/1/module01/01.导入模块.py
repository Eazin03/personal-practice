# 导入模块
# import random
# for i in range(10):
#     print(random.randint(1,100))

# 2.导入模块中的功能 from 。。。。 import 。。。---> 调用方式：别名

# import random
from random import randint
from random import *
for i in range(10):
    print(randint(1,100))