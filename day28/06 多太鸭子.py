# 1. 什么是多态？
    # 多态指的是一类事物有多种形态，比如动物有多种形态：猫、狗、猪
# class Animal:
#     def say(self):
#         print('动物的发生频率。。。', end='')

# class People(Animal):
#     pass       

# class Dog(Animal):
#     pass

# class Pig(Animal):
#     pass



# 2. 为何要有多态========多态性
        # 多态性指得是不考虑对象类型的情况下，直接使用对象

# class Animal:  # 统一所有子类的方法
#     def say(self):
#         print('动物的发生频率。。。', end='')

# class People(Animal):
#     def say(self):
#         super().say()
#         print('滋滋滋滋滋')        

# class Dog(Animal):
#     def say(self):
#         super().say()
#         print('汪汪汪') 

# class Pig(Animal):
#     def say(self):
#         super().say()
#         print('哼哼哼') 

# obj1=People()
# obj2=Dog()
# obj3=Pig()


# # 输出
# # 动物的发生频率。。。滋滋滋滋滋
# # 动物的发生频率。。。汪汪汪
# # 动物的发生频率。。。哼哼哼

# # 更进一步，定义统一的接口，接受传入的动物对象
# def animal_say(animal):
#     animal.say()


# animal_say(obj1)  # 直接传入对象
# animal_say(obj2)
# animal_say(obj3)

# 输出：
# 动物的发生频率。。。滋滋滋滋滋
# 动物的发生频率。。。汪汪汪
# 动物的发生频率。。。哼哼哼


# 但是python不是推崇继承的方式，来实现多态



# python应该这样用

# python推崇的是鸭子类型

class Cpu:
    def read(self):
        print('cpu read')
    def write(self):
        print('cpu write')

class Mem:
    def read(self):
        print('mem read')
    def write(self):
        print('mem write')   

class Txt:
    def read(self):
        print('txt read')
    def write(self):
        print('txt write')


obj1=Cpu()
obj2=Mem()
obj3=Txt()


obj1.read()
obj1.write()

obj2.read()
obj2.write()


obj3.read()
obj3.write()

# 输出
# cpu read
# cpu write
# mem read
# mem write
# txt read
# txt write