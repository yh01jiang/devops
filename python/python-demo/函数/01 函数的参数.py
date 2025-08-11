# # 形参即在定义函数时，括号内声明的参数。形参本质就是一个变量名，用来接收外部传来的值。相当于变量名
# def func(x,y):
#     print(x,y)
# # 实参即在调用函数时，括号内传入的值，值可以是常量、变量、表达式或三者的组合。相当于变量值
# func(1,2)




# def register(name,age,sex): #定义位置形参：name，age，sex，三者都必须被传值
#     print('Name:%s Age:%s Sex:%s' %(name,age,sex))
# register() #TypeError：缺少3个位置参数
# register('barry',18,'male')


# def func(x,y):
#     print(x,y)
# func(y=3,x=4)



# def func(x,y=1):
#     print(x,y)
# func(3)


# *args d的使用
# def func(x,y,*args):
#     print(x,y,args)
# func(1,2,3,4,5,6)  # 输出结果：1 2 (3, 4, 5, 6)




# def func(x,y,**kwargs):
#     print(x,y,kwargs)
# func(1,y=2,a=1,b=2,c=3)  # 输出结果: 1 2 {'a': 1, 'b': 2, 'c': 3}



# def func(x,y,z):
#     print(x,y,z)

# func(*[11,22,33])  # func(11,22,33)  # 打散


# def func(x,y,z):
#     print(x,y,z)

# func(*{'x':1, 'y':2, 'z':3 })  # 输出结果：x y z
# func(**{'x':1, 'y':2, 'z':3 })  #打散func(x=1,y=2,z=3) 输出结果：1 2 3




# def func():
#     a=111
#     b=222

# f1=func

# print(f1)


# input=333
# def func():
#     input=444


# func()  
# print(input)



# x=111

# def foo():
#     print(x, id(x))

# def bar():
#     print(x,id(x))

# foo()
# bar()
# print(x,id(x))

# 111 4341829296
# 111 4341829296
# 111 4341829296



# def f1():
#     n=999
#     def f2():
#         print(n)

#     return f2
# f=f1()
# f()





# import time
# def index(x,y):
#     time.sleep(3)
#     print('index %s %s' %(x,y))

# index(111,222)





# import time
# def index(x,y):
#     start=time.time()
#     time.sleep(3)
#     print('index %s %s' %(x,y))
#     stop=time.time()
#     print(stop - start )

# index(111,222)



# import time
# def index(x,y):
#     time.sleep(3)
#     print('index %s %s' %(x,y))

# start=time.time()
# index(111,222)
# stop=time.time()
# print(stop - start)



# import time
# def index(x,y):
#     time.sleep(3)
#     print('index %s %s' %(x,y))

# def wrapper():
#     start=time.time()
#     index(111,222)
#     stop=time.time()
#     print(stop - start)

# wrapper()



# 方案三的优化0：
# import time
# def index(x,y):
#     time.sleep(3)
#     print('index %s %s' %(x,y))
# def wrapper(a,b):  # a=111,b=222
#     start=time.time()
#     index(a,b)  # index(111,222)
#     stop=time.time()
#     print(stop - start)

# wrapper(111,222)



# import time
# def index(x,y,z):
#     time.sleep(3)
#     print('index %s %s %s' %(x,y,z))
# def wrapper(*args,**kwargs):
#     start=time.time()
#     index(*args,**kwargs)
#     stop=time.time()
#     print(stop - start)


# wrapper(333,444,555)
# wrapper(3333,y=4444,z=5555)




# 方案三的优化2：在优化1的基础上，把被装饰对象写活了，原来只能装饰index
import time
def index(x,y,z):
    time.sleep(3)
    print('index %s %s %s' %(x,y,z))
print(index)  # <function index at 0x023345D0>

def outter(func):
    # func=index的内存地址
    def wrapper(*args,**kwargs):
        start=time.time()
        func(*args,**kwargs)  # index内存地址()
        stop=time.time()
        print(stop - start)
    return wrapper  # 其实就是为了扔到全局，因为当初wrapper是全局，现在缩进了函数内。

index=outter(index)  # f=outter(index的内存地址)
print(index)  # <function outter.<locals>.wrapper at 0x01D0B660>
# f=当初那个wrapper函数的内存地址
index(11,22,33)
index(x=1,y=2,z=3)

