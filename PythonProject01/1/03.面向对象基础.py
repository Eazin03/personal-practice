# 定义类 -->不推荐
# class Car:
#     pass
#
#
# # 创建对象
# c1 = Car()
# c1.color = "red"
# c1.brand = "BMw"
# c1.name = "X5"
# c1.price = 15
# print(c1)
# print(c1.color)
# print(c1.__dict__) # 会将对象中的所有属性以字典的形式输出出啦
#
#
# # 定义类:
# class Car:
#     #__init__ 方法是初始化的方法,会在对象创建时自动调用,可以在该方法中为对象设置对应的属性
#     # self:是第一个参数,表示当前所创建出来的实例对象
#     def __init__(self,c_color, c_brand,c_price):
#         self.c_color = c_color
#         self.c_brand = c_brand
#         self.c_price = c_price
#         print("Car类型的对象初始化完毕,对象属性已经添加完毕")
#
# # 创建对象
# c1 = Car('red','BMW',15)
# print(c1.__dict__)
from operator import and_
from stringprep import c22_specials


class Car:
    # 类属性(所有实例对象共享); 通过实例对象,查找属性时,会先查找实例属性; 实例属性不存在,再查找类属性
    wheel = 4 #轮胎数量
    tax_rate = 0.1 # 购置税税率

    def __init__(self,c_color, c_brand,c_name,c_price):
        #实例属性
        self.color = c_color
        self.brand = c_brand
        self.name = c_name
        self.price = c_price
        self.wheel = 5

    def running(self):
        print(f"{self.brand} {self.name} 快速的蹦跑.....")

    def total_cost(self,discount,rate):
        """#输入三个双引号就能直接输出
        计算提车的总费用,包含两个部分:车的价格和税收
        :param discount:折扣
        :param rate:税率
        :return:提车的总费用
        """
        total_cost = self.price * discount + rate * self.price
        return total_cost

    # 魔法方法:自动调用
    def __str__(self):# 将内容输出为字符串形式
        return f"{self.color} {self.brand} {self.name} {self.price}"

    def __eq__(self, other):
        return self.price == other.price and self.brand == other.brand and self.name == other.name and self.color == other.color

    def __lt__(self, other):
        return self.price < other.price

# 测试

c1 = Car("red","BWM","X5",500)
print(c1)
print(c1.wheel) # 通过实例对象,查找属性时,会先查找实例属性; 实例属性不存在,再查找类属性

# 通过类名访问类属性
print(Car.wheel)

c2 = Car("red","BWM","X5",500)
print(c2)
# total = c1.total_cost(0.9,0.2)
# print(f"提车的总费用为{total:.0f}")
# c1.running()




print(c1 == c2)
print(c1 > c2)