# class People:

#     def __init__(self,name,weight,height):
#         self.name=name
#         self.weight=weight
#         self.height=height
    
#     # 定义函数的原因：
#     # 1. 从bmi的公式上看，应该是触发功能计算得到的
#     # 2. bmi是随着身高 体重变化的到的，不是一个固定的值，说白了，每次都是临时计算的到的 
    
#     # 但是bmi更像是一个数据属性，而不是一个功能
#     def bmi(self):
#         return self.weight / (self.height ** 2)
        
# obj=People('egon', 70, 1.8)


# print(obj.bmi())  # 21.604938271604937
 

# 案例1 

# # property是一个装饰器，是用来将绑定给对象的方法伪装成一个数据属性。

# class People:

#     def __init__(self,name,weight,height):
#         self.name=name
#         self.weight=weight
#         self.height=height
    
#     # 定义函数的原因：
#     # 1. 从bmi的公式上看，应该是触发功能计算得到的
#     # 2. bmi是随着身高 体重变化的到的，不是一个固定的值，说白了，每次都是临时计算的到的 
    
#     # 但是bmi更像是一个数据属性，而不是一个功能
#     @property   # 使用装饰器将绑定给对象的方法伪装成一个数据属性，下文就不需要再次调用obj.bmi()使用了
#     def bmi(self):
#         return self.weight / (self.height ** 2)
        
# obj=People('egon', 70, 1.8)


# print(obj.bmi)  # 21.604938271604937
     


# 案例2:

# class People:
#     def __init__(self,name):
#         self.__name=name  # 属性隐藏

#     # 开放接口
#     def get_name(self):
#         return self.__name

#     def set_name(self,val):
#         if type(val) is not str:
#             print('请传入字符串')
#             return
#         self.__name=val

#     def del_name(self):
#         print('不让删除')
#         del self.__name


# obj1=People('egon')
# print(obj1.get_name())
# obj1.set_name('EGON')
# print(obj1.get_name())
# obj1.del_name()

# # 输出结果：
# egon
# EGON
# 不让删除



# class People:
#     def __init__(self,name):
#         self.__name=name  # 属性隐藏

#     # 开放接口
#     def get_name(self):
#         return self.__name

#     def set_name(self,val):
#         if type(val) is not str:
#             print('请传入字符串')
#             return
#         self.__name=val

#     def del_name(self):
#         print('不让删除')
#         del self.__name

#     # 将绑定方法伪装策称一个数据属性，@property 代表的就是 函数=property(函数)
#     name=property(get_name,set_name,del_name)


# obj1=People('egon')

# print(obj1.name) # 其实就是找name属性中的get_name 的方法去执行，将name返回出去

# obj1.name = 18  #  其实就是找name属性中的set_name 方法的运行，set_name 需要两个参数，将obj1 以及 18 传给set_name 函数


# del obj1.name

# # 输出
# # egon
# # 请传入字符串
# # 不让删除


# 案例3:

# 首先对name 属性的三个访问操作，都定义成想让外部使用者访问的属性名字
class People:
    def __init__(self,name):
        self.__name=name  # 属性隐藏

    @property  # 其实就是执行了这种操作：name=property(name)
    def name(self):  # obj1.name
        return self.__name

    @name.setter
    def name(self,val):  # obj1.name = 'EGON'
        if type(val) is not str:
            print('请传入字符串')
            return
        self.__name=val

    @name.deleter
    def name(self):  # del obj1.name
        print('不让删除')
        del self.__name




obj1=People('egon')
# 人正常的思维逻辑
print(obj1.name) 

obj1.name = 18  
del obj1.name

# 输出：
# egon
# 请传入字符串
# 不让删除


