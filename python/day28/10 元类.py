# class People:

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))


# obj=People('egon', 38)
# print(obj.__dict__)  # {'name': 'egon', 'age': 38}
# print(type(obj))  # <class '__main__.People'>

# print(type(People))  # <class 'type'>


# print(type(int))  # <class 'type'>  默认的type就是元类

# 推导出
# People=元类(...)


# 三  class关键字创建类的流程分析
# 类的三大特征
# 1. 类名
# class_name="People"

# # 2. 类的父类
# class_bases=(object,)

# # 3. 执行类体代码拿到类的名称空间
# class_dic={}
# class_body="""
# def __init__(self,name,age):
#     self.name=name
#     self.age=age

# def say(self):
#     print('%s:%s' %(self.name,self.age))
# """

# exec(class_body, {}, class_dic)
# # print(class_dic)  # {'__init__': <function __init__ at 0x1044581f0>, 'say': <function say at 0x1044f8940>}

# # 4. 调用元类
# # print(type(class_name,class_bases,class_dic))  # <class '__main__.People'>
# People=type(class_name,class_bases,class_dic)


# obj=People('egon',18)
# print(obj.__dict__)  # {'name': 'egon', 'age': 18}

# print(obj.name)  # egon




# 四  如何自定义元类

# class Mymeta(type):  # 只有继承了type类的才是元类
#           #      空对象,People",(object),{...}
#     def __init__(self,x,y,z):  # 其实x y z 就是class_name,class_bases,class_dic，只是为了好区分，就是一个变量
#         print('run.....')
#         print(self)
#         print(x)
#         print(y)
#         print(z)

# 类的产生过程其实就是元类的调用过程
# # People=Mymeta(class_name,class_bases,class_dic)  ====》 其实是这样的：People=Mymeta("People",(object),{...})
# # 调用Mymeta发生的三件事：
# # 1. 先造一个空对象==》People
# # 2. 调用Mymeta类中的__init__方法，完成初始化对象的操作
# # 3. 返回初始化好的对象

# class People(metaclass=Mymeta):

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))


# 输出：
# run.....
# <class '__main__.People'>
# People
# ()
# {'__module__': '__main__', '__qualname__': 'People', '__init__': <function People.__init__ at 0x104338a60>, 'say': <function People.say at 0x104338af0>}




# 案例
# 必须类名首字母大写
# class Mymeta(type):  # 只有继承了type类的才是元类
#           #      空对象,People",(object),{...}
#     def __init__(self,x,y,z):  # 其实x y z 就是class_name,class_bases,class_dic，只是为了好区分，就是一个变量
#         if not x.istitle():
#             raise NameError('类名首字母必须大写。。。')
#         # print('run.....')
#         # print(self)
#         # print(x)
#         # print(y)
#         # print(z)


# class People(metaclass=Mymeta): # metaclass关键字参数为一个类指定元类

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))

# 输出
# 如果类名是people，就会主动抛出错误：
# Traceback (most recent call last):
#   File "/Users/jiangyuanhao/Desktop/project-demo/python-demo/day28/10 元类.py", line 110, in <module>
#     class people(metaclass=Mymeta):
#   File "/Users/jiangyuanhao/Desktop/project-demo/python-demo/day28/10 元类.py", line 102, in __init__
#     raise NameError('类名首字母必须大写。。。')
# NameError: 类名首字母必须大写。。。

# 如果类名是People: 就不会有报错





# # __new__  是产生一个空对象，是早于__init__ 产生的

# class Mymeta(type):  # 只有继承了type类的才是元类
#           #      空对象,People",(object),{...}
#     def __init__(self,x,y,z):  # 其实x y z 就是class_name,class_bases,class_dic，只是为了好区分，就是一个变量
#         if not x.istitle():
#             raise NameError('类名首字母必须大写。。。')
#         print(y)  # y就是People的基类  # 输出 ()
#         print(self.__bases__)  # (<class 'object'>,)
#     # def __new__(cls,*args,**kwargs):
#     #     pass


# # # People=Mymeta(class_name,class_bases,class_dic)  ====》 其实是这样的：People=Mymeta("People",(object),{...})
# # # 调用Mymeta(元类)发生的三件事：
# # # 1. 先造一个空对象==》People===> 调用类内的__new__ 方法
# # # 2. 调用Mymeta类中的__init__方法，完成初始化对象的操作
# # # 3. 返回初始化好的对象

# class People(metaclass=Mymeta):

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))






# class Mymeta(type):  # 只有继承了type类的才是元类
#           #      空对象,People",(object),{...}
#     def __init__(self,x,y,z):  # 其实x y z 就是class_name,class_bases,class_dic，只是为了好区分，就是一个变量
#         if not x.istitle():
#             raise NameError('类名首字母必须大写。。。')
#         print('run222222')
#         # print(y)  # y就是People的基类  # 输出 ()
#         # print(self.__bases__)  # (<class 'object'>,)

#         # 注意： 当前所在的类，调用类所传的参数
#     def __new__(cls,*args,**kwargs):
#         print('run 11111.')
#         # 造Mymeta的对象
#         # print('run11111...')  # run11111...
#         # print(cls,args,kwargs)  # <class '__main__.Mymeta'> People () {'__module__': '__main__', '__qualname__': 'People', '__init__': <function People.__init__ at 0x102bf8af0>, 'say': <function People.say at 0x102bf8b80>}
#         # return super().__new__(cls,*args,**kwargs)  # 从父类去找方式1:
#         return type.__new__(cls,*args,**kwargs)       # 从父类去找方式2:
#         # 会将这个对象cls,*args,**kwargs 传给__init__

# # # People=Mymeta(class_name,class_bases,class_dic)  ====》 其实是这样的：People=Mymeta("People",(object),{...})
# # # 调用Mymeta(元类)发生的三件事：
# # # 1. 先造一个空对象==》People===> 调用类内的__new__ 方法
# # # 2. 调用Mymeta类中的__init__方法，完成初始化对象的操作
# # # 3. 返回初始化好的对象

# class People(metaclass=Mymeta):

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))



# # 强调：
# # 只要是调用类，那么就会依次调用：
# # 1. 类内的__new__
# # 2. 类内的__init__



# __call__  方法

# 引入
# class Foo:
#     def __init__(self,x,y):
#         self.x=x
#         self.y=y


# obj=Foo(111,333)
# print(obj.__dict__)
# obj()  # 这样直接调用obj对象报错：TypeError: 'Foo' object is not callable，怎么解决呢？这时候就需要介入于__call__  方法解决


# class Foo:
#     def __init__(self,x,y):
#         self.x=x
#         self.y=y

#     def __call__(self):
#         print('====>')
#         return  123


# obj=Foo(111,333)
# print(obj) # obj.__str__
# res=obj()    # res=obj.__call__() (返回的NOne，也就是说明打印obj的返回值，其实几件事obj.__call__的返回值，例如返回123)
# print(res)   # 123


# __call__ 的应用： 如果想让一个对象可以加()调用，需要在该对象的类中添加一个方法__call__

 
# class Foo:
#     def __init__(self,x,y):
#         self.x=x
#         self.y=y

#                 #obj 1,2,3,a=2,b=3
#     def __call__(self,*args,**kwargs):
#         print('====>', args, kwargs)  # ====> (1, 2, 3) {'a': 2, 'b': 3}
#         return  1234567890


# obj=Foo(111,333)
# res=obj(1,2,3,a=2,b=3)   # res=obj.__call__()
# print(res)  # 1234567890


# 总结

# 对象() ===> 类内的__call__
# 类() ====> 自定义元类的__call__
# 自定义元类() =====> 内置元类的__call__


# 6. 自定义元类控制类的调用：===》类的对象的产生
# class Mymeta(type):  # 只有继承了type类的才是元类

#     def __init__(self,x,y,z):  
#         print('run222222。。。。')

#     def __new__(cls,*args,**kwargs):
#         print('run 11111.。。。。')
#         # return super().__new__(cls,*args,**kwargs)  
#         return type.__new__(cls,*args,**kwargs)     


# # 一 类的产生：
# # People=Mymeta() ==> type.__call__===>干了三件事：
# # 1. type.__call__函数内会先调用Mymeta内的__new__
# # 2. type.__call__函数内会先调用Mymeta内的__init__
# # 3.  type.__call__函数内返回一个初始化好的对象
# class People(metaclass=Mymeta):

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))






class Mymeta(type):  # 只有继承了type类的才是元类

    def __call__(self,*args,**kwargs):

        # 1. Mymeta.__call__函数内会先调用People内的__new__
        people_obj=self.__new__(self)
        # 2. Mymeta.__call__函数内会先调用People内的__init__
        self.__init__(people_obj,*args,**kwargs)
        
        print('people对象属性： ', people_obj.__dict__)  # people对象属性：  {'name': 'egon', 'age': 18}
        people_obj.__dict__['xxxxx']=1111111
        # 3. Mymeta.__call__函数内返回一个初始化好的对象
        return people_obj
        # print(self)  # <class '__main__.People'>
        # print(args)  # ('egon', 18)
        # print(kwargs)  # {}
        # return 123456



# # 一 类的产生：
# # People=Mymeta() ==> type.__call__===>干了三件事：
# # 1. type.__call__函数内会先调用Mymeta内的__new__
# # 2. type.__call__函数内会先调用Mymeta内的__init__
# # 3.  type.__call__函数内返回一个初始化好的对象
# class People(metaclass=Mymeta):

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s:%s' %(self.name,self.age))

#     # 产生真正的对象（使用object的方法）
                # cls 自己的类
#     def __new__(cls,*args,**kwargs):
#         return object.__new__(cls)

# # 二 类的调用
# # obj=People('egon',18)  ==》Mymeta.__call__ ===》 干了三件事
# # 1. Mymeta.__call__函数内会先调用People内的__new__
# # 2. Mymeta.__call__函数内会先调用People内的__init__
# # 3. Mymeta.__call__函数内返回一个初始化好的对象


# # obj=People('egon',18)

# # # print(obj) 
# # print(obj.__dict__)  # {'name': 'egon', 'age': 18}

# obj1=People('egon', 18)
# obj2=People('egon',20)

# print(obj1.__dict__)
# print(obj2.__dict__)

# # 输出
# {'name': 'egon', 'age': 18, 'xxxxx': 1111111}
# {'name': 'egon', 'age': 20, 'xxxxx': 1111111}



# 属性查找
# class Mymeta(type): #只有继承了type类才能称之为一个元类，否则就是一个普通的自定义类
#     n=444

# class Bar(object):
#     n=333

# class Foo(Bar):
#     n=222
   

# class StanfordTeacher(Foo,metaclass=Mymeta):
#     n=111

#     school='Stanford'

#     def __init__(self,name,age):
#         self.name=name
#         self.age=age

#     def say(self):
#         print('%s says welcome to the Stanford to learn Python' %self.name)


# # 按对象查找
# obj=StanfordTeacher('egon',18)
# print(obj.n)  # 查找顺序：StanfordTeacher->Foo->Bar->object 如果object没有的就找不到了


# # 按类的查找
# # print(StanfordTeacher.n)



class Mymeta(type): 
    n=444
                # self指的是Mymeta对象，Mymeta的对象就是StanfordTeacher
    def __call__(self, *args, **kwargs): #self=<class '__main__.StanfordTeacher'>
        obj=self.__new__(self)  # 推荐使用这种方式   # StanfordTeacher.__new__
        # obj=object.__new__(self)  # 不推荐这种方式
        # print(self.__new__ is object.__new__) #True
        self.__init__(obj,*args,**kwargs)
        return obj


class Bar(object):
    n=333

    # def __new__(cls, *args, **kwargs):
    #     print('Bar.__new__')

class Foo(Bar):
    n=222

    # def __new__(cls, *args, **kwargs):
    #     print('Foo.__new__')

class StanfordTeacher(Foo,metaclass=Mymeta):
    n=111

    school='Stanford'

    def __init__(self,name,age):
        self.name=name
        self.age=age

    def say(self):
        print('%s says welcome to the Stanford to learn Python' %self.name)


    def __new__(cls, *args, **kwargs):
    #     print('StanfordTeacher.__new__')
        return object.__new__(cls)


obj=StanfordTeacher('lili',18) #触发StanfordTeacher的类中的__call__方法的执行，进而执行self.__new__开始查找
print(obj.__dict__)  # {'name': 'lili', 'age': 18}