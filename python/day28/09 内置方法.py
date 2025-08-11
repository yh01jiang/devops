# 1. 什么是内置方法？
# 定义在类内部，以__开头并以__结尾的方法
# 特点； 会在某种情况下自动出发

# 2. 为何要用内置方法？
# 为了定制化我们的类或者对象

# 3. 如何使用内置方法




# __str__
# class People:
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))

# obj=People('辣白菜同学', 18)
# print(obj)  # <__main__.People object at 0x100b5afd0>


# 这就是__str__ 的特性: 在打印对象时会自动触发，并将返回值（必须是字符串类型）当作本次打印的结果输出
# class People:
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def __str__(self):
#         # print('运行了。。。。')
#         # return 'hahhahhhaha a'
#         return '%s:%s' %(self.name,self.age)

# obj=People('辣白菜同学', 18)
# # print(obj.__str__())  # 辣白菜同学:18
# print(obj)  # 辣白菜同学:18





# __del__ ： 在清理对象时触发，会先执行该方法
# class People:
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def __del__(self):
#         print('运行了。。。')
# obj=People('辣白菜同学', 18)
# print('==========>')

# # 输出：
# # ==========>
# # 运行了。。。



class People:
    def __init__(self,name,age):
        self.name=name
        self.age=age
        # self.x=open('a.txt',mode='w')
        # self.x = 占据的是操作系统的资源

    def __del__(self):
        print('运行了。。。')
        # 发起系统调用，告诉操作系统回收相关的资源
        # self.x.close()
obj=People('辣白菜同学', 18)

del obj
print('=================>')

# 输出：
# 运行了。。。
# =================>



class People:
    def __init__(self,name,age):
        self.name=name
        self.age=age
        # self.x=open('a.txt',mode='w')
        # self.x = 占据的是操作系统的资源

    def __del__(self):
        print('运行了。。。')
        # 发起系统调用，告诉操作系统回收相关的资源
        # self.x.close()
obj=People('辣白菜同学', 18)

del obj
print('=================>')