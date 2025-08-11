# print(complex('1+2j'))

# print(complex())

# print(complex(1,2))

# print(complex(2))



# class Test:
#     def  f1():
#         return 1
    
#     def f2():
#         return 2
    

# print(dir(Test))
# print(dir())



# stu = ['xiao','zhang','li','qian']


# print(enumerate(stu))

# print(list(enumerate(stu)))

# print(list(enumerate(stu, start=1)))


# print(eval("1+1"))

# print(eval("1==1"))


# num_list = list(range(10))
# print(num_list)


# def mod_three(num):
#     if (num%3==0):
#         return True
#     else:
#         return False



# print(filter(mod_three,num_list))
# print(list(filter(mod_three,num_list)))



# num = 1234567890
# print(isinstance(num,str))
# print(isinstance(num,int))


# def fun_a(a,b):
#     return a+2*b

# num_list1=[1,2,3,4]
# num_list2=[2,3,4,5]
# print(list(map(fun_a,num_list1,num_list2)))




# s1 = input('input:')
# print(s1)



num_list1 = [1,2,3,4]
num_list2 = [2,3,1,2]

res=list(zip(num_list1,num_list2))
print(res)