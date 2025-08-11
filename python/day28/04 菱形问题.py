# 示例1:
# class A():
#     def test(self):
#         print('from A')


# class B(A):
#     def test(self):
#         print('from B')


# class C(A):
#     def test(self):
#         print('from C')


# class D(B,C):
#     pass


# obj = D()
# obj.test()  # from B

# print(D.__mro__)  # (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)


# 示例2:
# class A(object):
#     def test(self):
#         print('from A')


# class B(A):
#     # 如果注释掉B类的test() ，那么就会无下一个C类里面去找test()方法
#     pass


# class C(A):
#     def test(self):
#         print('from C')


# class D(B,C):
#     pass


# obj = D()
# obj.test()  # from C


# 示例3:
# class A(object):
#     def test(self):
#         print('from A')


# class B(A):
#     # 如果注释掉B类的test() ，那么就会无下一个C类里面去找test()方法
#     pass


# class C(A):
#      # 如果注释掉C类的test() ，那么就会无下一个A类里面去找test()方法
#      pass
    


# class D(B,C):
#     pass


# obj = D()
# obj.test()  # from A



# class E:
#     def test(self):
#         print('from E')


# class F:
#     def test(self):
#         print('from F')


# class B(E):
#     def test(self):
#         print('from B')


# class C(F):
#     def test(self):
#         print('from C')


# class D:
#     def test(self):
#         print('from D')


# class A(B, C, D):
#     # def test(self):
#     #     print('from A')
#     pass


# print(A.mro())
# # [<class '__main__.A'>, <class '__main__.B'>, <class '__main__.E'>, <class '__main__.C'>, <class '__main__.F'>, <class '__main__.D'>, <class 'object'>]


# obj = A()
# obj.test()  # # 结果为：from B
# # 可依次注释上述类中的方法test来进行验证



# class G(object):
#     def test(self):
#         print('from G')

# class E(G):
#     def test(self):
#         print('from E')

# class F(G):
#     def test(self):
#         print('from F')

# class B(E):
#     def test(self):
#         print('from B')

# class C(F):
#     def test(self):
#         print('from C')

# class D(G):
#     def test(self):
#         print('from D')

# class A(B,C,D):
#     # def test(self):
#     #     print('from A')
#     pass

# obj = A()
# obj.test() # 如上图，查找顺序为:obj->A->B->E->C->F->D->G->object
# # 可依次注释上述类中的方法test来进行验证\
# print(A.__mro__)
# # (<class '__main__.A'>, <class '__main__.B'>, <class '__main__.E'>, <class '__main__.C'>, <class '__main__.F'>, <class '__main__.D'>, <class '__main__.G'>, <class 'object'>)




# # 定义父类
# class initial(object):
#     def __init__(self):
#         print ('This print is from initial object')
#         # 定义父类参数
#         self.param = 3

#     # 定义父类函数
#     def func(self):
#         return 1

# # 定义子类
# class new(initial):
#     def __init__(self):
#         print ('This print is from new object')
#         # 打印子类函数值
#         print (self.func())
#         # 执行父类初始化函数
#         super(new, self).__init__()
#         # 打印父类参数值
#         print(self.param)
#         self.param = 4

#     # # 定义子类函数
#     # def func(self):
#     #     return 2

# # if __name__ == '__main__':
# #     new()


# obj=new()

# print(obj.__dict__)


