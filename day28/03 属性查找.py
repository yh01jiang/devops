
# class Foo():
#     def f1(self):
#         print('我是在Foo.f1')
    
#     def f2(self):
#         print('我是在Foo.f2')

# class Bar(Foo):
#     def f1(self):
#         print('我是在Bar.f1')

# obj=Bar()

# obj.f2()  # 我是在Foo.f2
# obj.f1()  # 我是在Bar.f1

# obj.f2()会在父类Foo中找到f2，先打印Foo.f2,然后执行到self.f1(),即obj.f1()，
# 仍会按照：对象本身->类Bar->父类Foo的顺序依次找下去，在类Bar中找到f1，因而打印结果为Bar.f1


# 父类如果不想让子类覆盖自己的方法，可以采用双下划线开头的方式将方法设置为私有的



class Foo():
    def __f1(self):  # 变形为_Foo__f1
        print('我是在Foo.f1')
    
    def f2(self):
        print('我是在Foo.f2')
        #  通过开放该接口就可以访问到名字属性（隐藏）
        self.__f1()  # 变形为self._Foo__f1,因而只会调用自己所在的类中的方法
class Bar(Foo):
    def __f1(self):  # # 变形为_Bar__f1
        print('我是在Bar.f1')


obj2=Bar()
obj2.f2()  #在父类中找到f2方法，进而调用._Foo__f1()方法，同样是在父类中找到该方法


print(Bar._Bar__f1)

# 输出
# 我是在Foo.f2
# 我是在Foo.f1
# <function Bar.__f1 at 0x102fcca60>
