# class Vehicle:  # 交通工具
#     pass

# class CivilAircraft(Vehicle):  # 民航飞机
#     pass


# class Helicopter(Vehicle):  # 直升飞机
#     pass


# class Car(Vehicle):  # 汽车并不会飞，但按照上述继承关系，汽车也能飞了
#     pass



# 优化：

# class Vehicle:  # 交通工具
#     pass


# class FlyableMixin:  # 在Flyable后面加入Mixin，就是明确告诉这个类是Mixin类，是作为功能添加到子类中，而不是作为父类。说白了就是一个功能类。
#     def fly(self):
#         '''
#         飞行功能相应的代码        
#         '''
#         print("I am flying")


# class CivilAircraft(FlyableMixin, Vehicle):  # 民航飞机
#     pass


# class Helicopter(FlyableMixin, Vehicle):  # 直升飞机
#     pass


# class Car(Vehicle):  # 汽车
#     pass

# ps: 采用某种规范（如命名规范）来解决具体的问题是python惯用的套路







#1. 在子类派生的方法中如何重用父类的功能
# 方式1: 指名道姓的调用某一个类下的函数==》不依赖于继承关系
# class OldboyPeople():
#     school = "OLDBOY"
 
#     def __init__(self,name,age,sex):
#         self.name=name
#         self.age=age
#         self.sex=sex

#     def f1(self):
#         print('%s say hello'  %(self.name))



    
# class Teacher(OldboyPeople):

#     def __init__(self,name,age,sex,salary,level):
#         OldboyPeople.__init__(self,name,age,sex)
#         self.salary=salary
#         self.level=level


# obj=Teacher('egon',18,'male',3000,10)
# print(obj.__dict__)

# # 输出：
# # {'name': 'egon', 'age': 18, 'sex': 'male', 'salary': 3000, 'level': 10}

# # 方式2: super()调用父类提供给自己的方法===》严格依赖继承关系
# #         调用super()会得到一个特殊的对象，该对象专门用来引用父类的属性，且严格按照发起属性查找类的那个MRO,去当前类的父类去找
# class OldboyPeople():
#     school = "OLDBOY"
 
#     def __init__(self,name,age,sex):
#         self.name=name
#         self.age=age
#         self.sex=sex

#     def f1(self):
#         print('%s say hello'  %(self.name))



    
# class Teacher(OldboyPeople):

#     def __init__(self,name,age,sex,salary,level):
#         # 这是在python2 中的写法
#         # super(Teacher,self).__init__(name,age,sex)  # 调用的是方法，自动传入对象
#         # python3 中的方法
#         super().__init__(name,age,sex)
#         self.salary=salary
#         self.level=level

# print(Teacher.mro())

# tea_obj=Teacher('egon',18,'male',3000,10)
# print(tea_obj.__dict__)

# 输出
# [<class '__main__.Teacher'>, <class '__main__.OldboyPeople'>, <class 'object'>]
# {'name': 'egon', 'age': 18, 'sex': 'male', 'salary': 3000, 'level': 10}



#A没有继承B
class A:
    def test(self):
        super().test()

class B:
    def test(self):
        print('from B')

class C(A,B):
    pass

C.mro() # 在代码层面A并不是B的子类，但从MRO列表来看，属性查找时，就是按照顺序C->A->B->object，B就相当于A的“父类”
# [<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,<class ‘object'>]
obj=C()
obj.test() # 属性查找的发起者是类C的对象obj，所以中途发生的属性查找都是参照C.mro()
# 输出
# from B