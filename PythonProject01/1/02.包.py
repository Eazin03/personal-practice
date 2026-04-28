# 导入模块
# import utils.my_fun
# utils.my_fun.log_deparator1()
#
# from utils import my_fun
# my_fun.log_deparator3()

# 注意:如果要通过from utils import * 导入包下所有的模块,需要在__init__中导入__all__
from utils import *
my_fun.log_deparator3()
print(my_var.PI)

# 2.导入模块中的功能
# 相对路径:从当前文件所在目录开始查找;绝对路径: 从项目的根目录下开始查找
from utils.my_fun import log_deparator3
log_deparator3()