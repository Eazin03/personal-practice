# __all__ 指定from ... import * 导入的是哪些功能
__all__ = ["log_deparator1", "log_deparator2", "log_deparator3"]


# 常量（不会发生变化的数据 ; 常量的名称为全部大写）
PI = 3.14159
NAME = "yangzj"

# 函数
def log_deparator1():
    print("- " * 30)


def log_deparator2():
    print("+ " * 30)


def log_deparator3():
    print("= " * 30)


def log_deparator4():
    print("# " * 30)

# 测试函数
# __name__ : Python中的内置变量，表示的当前模块的名字（直接运行当前模块，__name__的值为“__main__"； 当前模块被导入时，__name__的值就是模块名
# 执行当前文件，则会执行如下代码；如果被当做模块导入,如下代码不执行;
if __name__ == "__main__":# 直接输入main就会有快捷键
    print(__name__)
    log_deparator1()