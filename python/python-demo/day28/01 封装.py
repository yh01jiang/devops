
# 我们之前所说的”整合“二字其实就是封装的通俗说法。
# 除此之外，针对封装到对象或者类中的属性，我们还可以严格控制对它们的访问，分两步实现：隐藏与开放接口


# 二 封装的属性如何隐藏操作
# 1. 如何隐藏：在属性名前面加__前缀，就会实现对外隐藏属性的效果
# 2. 该隐藏需要注意的问题：
#I、在类外部无法直接访问双下滑线开头的属性，但知道了类名和属性名就可以拼出名字：_类名__属性，然后就可以访问了，如Foo._Foo__x，所以说这种操作并没有严格意义上地限制外部访问，仅仅只是一种语法意义上的变形。
# class Foo:
#     __x = 1  # _Foo__x
#     def __f1():  # _Foo__f1
#         print('from test') 


# # 在外部通过_类__属性可以访问到，但是没有意义
# print(Foo._Foo__x)
# print(Foo._Foo__f1)

# 输出：
# 1
# <function Foo.__f1 at 0x10504c940>

# {'__module__': '__main__', '_Foo__x': 1, '_Foo__f1': <function Foo.__f1 at 0x104f44940>, '__dict__': <attribute '__dict__' of 'Foo' objects>, '__weakref__': <attribute '__weakref__' of 'Foo' objects>, '__doc__': None}
# Foo.x
# Foo.f1()

# II: 这种隐藏对外不对内,在类内部是可以直接访问双下滑线开头的属性的，比如self.__f1()，因为在类定义阶段类内部双下滑线开头的属性统一发生了变形。
# 因为__开头的属性会在检查类内的代码语法时统一发生变形
# class Foo:
#     __x = 1  # _Foo__x = 1

#     def __f1(self):  # _Foo__f1
#         print('from test') 
    
#     def f2(self):
#         print(self.__x) # print(self._Foo__x)
#         print(self.__f1) # print(self._Foo__f1)


# obj=Foo()
# obj.f2()

# # 结果：
# # 1
# # <bound method Foo.__f1 of <__main__.Foo object at 0x104c6aee0>>

# III:这种变形操作只在检查类体语法时候发生一次，之后__开头的属性不会发生改变
# class Foo:
#     __x = 1  # _Foo__x = 1

#     def __f1(self):  # _Foo__f1
#         print('from test') 
    
#     def f2(self):
#         print(self.__x) # print(self._Foo__x)
#         print(self.__f1) # print(self._Foo__f1)

# Foo.__y=3

# print(Foo.__dict__)
# print(Foo.__y)
# 输出
# {'__module__': '__main__', '_Foo__x': 1, '_Foo__f1': <function Foo.__f1 at 0x10021c940>, 'f2': <function Foo.f2 at 0x10021c9d0>, '__dict__': <attribute '__dict__' of 'Foo' objects>, '__weakref__': <attribute '__weakref__' of 'Foo' objects>, '__doc__': None, '__y': 3}
# 3





# class Foo:
#     __x = 1  
#     def __init__(self,name,age):  
#         self.name=name
#         self.age=age

# obj=Foo('egon', 18)
# print(obj.__dict__)
# print(obj.name,obj.age)
# # 输出
# # {'name': 'egon', 'age': 18}
# # egon 18



# class Foo:
#     __x = 1  
#     def __init__(self,name,age):  
#         self.__name=name
#         self.__age=age

#     def func(self):
#         print(self.__name)
#         print(self.__age)

# obj=Foo('egon', 18)
# print(obj.__dict__)
# print(obj.func)
# print(obj.name,obj.age)
# 输出结果：
# {'_Foo__name': 'egon', '_Foo__age': 18}
# <bound method Foo.func of <__main__.Foo object at 0x104e72fd0>>

# 3. 为何要隐藏？
# 将数据隐藏起来就限制了类外部对数据的直接操作，
# 然后类内应该提供相应的接口来允许类外部间接地操作数据，接口之上可以附加额外的逻辑来对数据的操作进行严格地控制
# I 隐藏数据属性
# 设计者

# class People:
#     def __init__(self,name):
#         # self.name=name
#         self.__name=name

#     def get_name(self):
#             # 通过该接口就可以访问到名字属性
#         # print('小垃圾，不让看')
#         print(self.__name)

#     def set_name(self,val):
#         self.__name=val
        


# obj=People('egon')
# # print(obj.name) # 无法直接用名字属性
# # obj.get_name()  # egon
# obj.set_name('EGON')
# obj.get_name()




class People:
    def __init__(self,name):
        # self.name=name
        self.__name=name

    def get_name(self):
            # 通过该接口就可以访问到名字属性
        # print('小垃圾，不让看')
        print(self.__name)

    def set_name(self,val):
        if type(val) is not str:
            print('小垃圾，必须传字符串类型')
            return
        self.__name=val

obj=People('egon')
obj.set_name(1234567890)  #因为这里不是字符串
obj.get_name()

# 输出：
# 小垃圾，必须传字符串类型
# egon      


# II 隐藏函数属性
