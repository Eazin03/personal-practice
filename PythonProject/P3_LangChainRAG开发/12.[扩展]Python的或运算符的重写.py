from hmac import trans_36


class Test( object):
    def __init__(self,name):
        self.name = name

    def __or__(self,other):
        return MySequence(self,other)

    def __str__(self):
        return self.name

class MySequence(object):
    def __init__(self,*args):# *args: 可变参数,可以添加任意个数参数
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)

    def __or__(self,other):
        self.sequence.append(other)
        return self # 返回对象本身

    def run(self):
        for item in self.sequence:
            print(item)

if __name__ == '__main__':
    t1 = Test('t1')
    t2 = Test('t2')
    t3 = Test('t3')
    t4 = Test('t4')
    t5 = Test('t5')
    t6 = Test('t6')

    d = t1 | t2 | t3 | t4 | t5 | t6
    d.run()