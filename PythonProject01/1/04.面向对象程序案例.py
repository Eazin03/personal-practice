from itertools import chain
from os import name
from platform import node
from re import match


class Student:
    def __init__(self,name,chinese,math,english):
        self.name=name
        self.chinese=chinese
        self.math=math
        self.english=english

    def __str__(self):
        return f'姓名: {self.name} | 语文: {self.chinese} | 数学: {self.math} | 英语: {self.english} | 总分: {self.chinese + self.math + self.english}'

    def update_score(self,chinese = None,math = None,english = None):
        self.chinese = chinese
        self.math = math
        self.english = english


class EguManage:
    verson = "1.0.0"

    def __init__(self):
        self.data = []

    def add_student(self):
        name=input("请输入学生姓名: ")
        for i in self.data:
            if i.name == name:
                print("学生姓名已经存在")
                return
        chinese=int(input("请输入学生语文成绩: "))
        math=int(input("请输入学生数学成绩: "))
        english=int(input("请输入学生英语成绩: "))

        if 0 <= chinese <=100 and 0 <= math <= 100 and 0 <= english <= 100:
            stu = Student(name,chinese,math,english)
            self.data.append(stu)
            print(stu)


    def update_student(self):
        name = input("请输入要修改的学生姓名: ")
        for i in self.data:
            if i.name == name:
                print(f'当前成绩: {i}')


                chinese = int(input("请输入要修改的语文成绩: "))
                math = int(input("请输入要修改的数学成绩: "))
                english = int(input("请输入要修改的英语成绩: "))
                if 0 <= chinese <=100 and 0 <= math <= 100 and 0 <= english <= 100:
                    i.update_score(chinese,math,english)
                    print("修改成功!")
                else:
                    print("成绩未在范围内")
            else:
                print("没有找到该学生")

    def del_student(self):
        name = input("请输入要删除的学生姓名: ")
        for i in self.data:
            if i.name == name:
                self.data.remove(i)
                print("删除成功!")
                return
        print("未找到学生信息")

    def query_student(self):
        name = input("请输入要查询的学生姓名: ")
        for i in self.data:
            if i.name == name:
                print(i)
            else:
                print("未查询到该学生信息!")

    def show_student(self):
        for i in self.data:
            print(i)

    def run(self):
        print(f'欢迎进入教务管理系统{EguManage.verson}!!!')

        while True:
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ")
            print("# 1.添加学生 2.修改学生 3.删除学生 4.查询指定学生 5.查询所有学生 6.退出系统 #")
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ")

            choice = int(input("请选择要执行的操作: "))
            try:
                match choice:
                    case 1:# 添加学生
                        self.add_student()
                    case 2:# 修改学生
                        self.update_student()
                    case 3:# 删除学生
                        self.del_student()
                    case 4:# 查询指定学生
                        self.query_student()
                    case 5:# 查询所有学生
                        self.show_student()
                    case 6:# 退出系统
                        break
                    case _:
                        print("请输入1-6范围内的数字")
            except ValueError:
                print("数据输入错误了,请重新输入!")
            except Exception as e:
                print("程序运行错误,请重新选择")

# 测试
if __name__ == '__main__':
    egu = EguManage()
    egu.run()