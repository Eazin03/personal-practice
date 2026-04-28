# 异常处理
# try:
#     print("========================")
#     print(my_name)
#     print("========================")
# except NameError as e:# 捕获的是NameError类型的错误
#     print("程序错误,请联系管理员",e)
#
from utils import my_fun


# try:
#     print("========================")
#     # print(1 / 0)
#     # print("ab"[10])
#     print('ABC'.hello)
#     print("========================")
# except NameError as e:# 捕获的是NameError类型的错误
#     print("名字不存在,请检查变量或函数名字,异常信息",e)
# except ZeroDivisionError as e:# 捕获的是值发生错误
#     print("0不能做被除数,异常信息: ",e)
# except IndexError as e:
#     print("索引出现错误",e)
# except Exception as e:# 捕获所有的异常
#     print("程序出现错误",e)
#
# finally: # 无论程序是否正常运行,finally都会运行
#     print("资源释放~")

def fun1():
    print("fun1...running....")
    fun2()

def fun2():
    print("fun2...running....")
    fun3()

def fun3():
    print("fun3...running....")
    print(my_name)


if __name__ == '__main__':
    try:
        fun1()
    except Exception as e:
        print(e)
