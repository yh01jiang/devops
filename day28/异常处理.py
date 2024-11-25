# print(x)
# count=0
# if count > 90
#     pass

# x

# l=[111,222]
# l[2]


# dic={'name': 'egon'}
# dic['age']

# print('start。。。。。')
# try:

#     print(x)

#     l=[111,222]
#     l[2]


#     dic={'name': 'egon'}
#     dic['age']

#     class Foo:
#         pass

#     Foo.x



# # except (NameError,IndexError,KeyError) as e:
# #     print('异常值： %s' %e)


# except NameError as e:
#     print('异常值为： %s' %e)
# except IndexError as e:
#     print('异常值为： %s' %e)
# except KeyError as e:
#     print('异常值为： %s' %e)
# except AttributeError as e:
#     print('异常值为：%s'  %e)
    
# # except Exception as e:
# #     print('异常值为： %s' %e)
    

# print('end。。。。。')


# 输出：
# start。。。。。
# 异常值： name 'x' is not defined
# end。。。。。



# print('start。。。。。')
# try:
#     x=10
#     print(x)

#     l=[111,222]
#     l[1]


#     dic={'name': 'egon'}
#     dic['name']

#     class Foo:
#         x=0

#     Foo.x



# except Exception as e:
#     print('异常值为： %s' %e)

# else:
#     print('如果没有异常，就执行到我这里')

# print('end。。。。。')

# 输出
# start。。。。。
# 10
# 如果没有异常，就执行到我这里
# end。。。。。





# print('start。。。。。')
# try:

#     print(x)

#     l=[111,222]
#     l[2]


#     dic={'name': 'egon'}
#     dic['age']

#     class Foo:
#         pass

#     Foo.x

 

# except Exception as e:
#     print('异常值： %s' %e)

# finally:
#     print('不管代码是否异常，都会执行此finally块代码')

# print('end。。。。。')

# 输出

# start。。。。。
# 异常值： name 'x' is not defined
# 不管代码是否异常，都会执行此finally块代码
# end。。。。。


# class Student:
#     def __init__(self,name,age):
#         if not isinstance(name,str):
#             raise TypeError('name must be str')
            
#         if not isinstance(age,int):
#             raise TypeError('age must be int')

#         self.name=name
#         self.age=age

# stu1=Student(4573,18) # TypeError: name must be str
# stu2=Student('egon','18') # TypeError: age must be int



# import time
 
# i = 0
# while True:
#     print(i)
#     i += 1
#     time.sleep(10)


# import schedule
# import time

# def do_func():

#     print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" in do func ...")

# def main():
#     schedule.every(2).seconds.do(do_func)

#     while True:
#         schedule.run_pending()

# if __name__=="__main__":
#     main()
