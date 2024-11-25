# # """
# 输入M和N计算C(M,N)

# Version: 0.1
# # Author: 骆昊
# # """
# def fac(num):
#     result = 1
#     for n in range(1, num + 1):
#         result *= n
#     return result


# m = int(input('m = '))
# n = int(input('n = '))
# # 当需要计算阶乘的时候不用再写循环求阶乘而是直接调用已经定义好的函数
# print(fac(m) // fac(n) // fac(m - n))



# result = 1
# for n in range(1, 5):  # 1 2 3 4
#     result *= n
# print(result)


# a *=b ======> a = a * b

# result = result * n

# # 1 = 1 * 1

# # 1 * 2 =2
# # 2* 3 =6 
# 6* 4 = 24 / 2 /2 






# from random import randint

# def roll_dice(n=2):
#     """摇色子"""
#     total = 0
#     for _ in range(n):
#         total += randint(1, 6)
#     return total

# print(roll_dice(3))



# def add(x,y):
#     res=x+y
#     return res
# res=add(20,30)
# print(res)





# # 案例1
# def my_sum(*args):
#     sum=0
#     for item in args:
#         sum+=item
#     return sum
# res=my_sum(1,2,3,4,5,6,7,8,9)
# print(res)  # 输出结果： 36



# def foo():
#     b = 'hello'

#     # Python中可以在函数内部再定义函数
#     def bar():
#         c = True
#         print(a)
#         print(b)
#         print(c)

#     bar()
#     # print(c)  # NameError: name 'c' is not defined


# if __name__ == '__main__':
#     a = 100
#     # print(b)  # NameError: name 'b' is not defined
#     foo()


# list1 = [1, 3, 5, 7, 100]
# # print(list1) # [1, 3, 5, 7, 100]
# for index in range(len(list1)):
#     print(list1[index])

# for elem in list1:
#     print(elem)


# import   os
# import time

# def main():
#     content = '北京欢迎你为你开天辟地............'
#     while True:
#         os.system('cls')
#         print(content)
#         time.sleep(0.4)
#         content = content[1:] + content[0]

# if __name__ == '__main__':
#     main()



# import random


# def generate_code(code_len=4):
#     """
#     生成指定长度的验证码

#     :param code_len: 验证码的长度(默认4个字符)

#     :return: 由大小写英文字母和数字构成的随机验证码
#     """
#     all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     last_pos = len(all_chars) - 1
#     code = ''
#     for _ in range(code_len):
#         index = random.randint(0, last_pos)
#         code += all_chars[index]
#     return code

# if __name__ == '__main__':
#     res=generate_code(6)
#     print(res)