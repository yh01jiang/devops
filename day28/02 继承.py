# class Animal:
#     def run(self):
#         print('奔跑')

#     def eat(self):
#         print('吃东西')


# class Duck:
#     def run(self):
#         print('奔跑')

#     def eat(self):
#         print('吃东西')

#     def speak(self):
#         print('嘎嘎嘎')

# class Pig:
#     def run(self):
#         print('奔跑')

#     def eat(self):
#         print('吃东西')

#     def speak(self):
#         print('咕咕咕')


# class Person:
#     def run(self):
#         print('奔跑')

#     def eat(self):
#         print('吃东西')

#     def speak(self):
#         print('呵呵呵')



# # 🍔使用继承编写多个类
# class Animal:
#     def run(self):
#         print("奔跑")

#     def eat(self):
#         print("吃东西")
        
# class Duck(Animal):
#     def speak(self):
#         print("嘎嘎嘎")
    
# class Pig(Animal):
#     def speak(self):
#         print("咕咕咕")
        
# class Person(Animal):
#     def speak(self):
#         print("呵呵呵")
        
# # 🔰#可以明显感觉到代码量减少     


# obj=Animal()
# obj.run()


# obj1=Duck()
# obj1.speak()
# obj1.run()
# # 输出：
# # 跑
# # 嘎嘎嘎
# # 奔跑

# 查看对象继承的类
# print(Person.__base__)  # <class '__main__.Animal'>




# class Shawn:
#     def Am(self):
#         print("i am from Shawn")

# class Pai:
#     def Am(self):
#         print("i am from Pai")

# class Da:
#     def Am(self):
#         print("i am from Da")

# class Xing(Pai,Shawn,Da):  # 继承了三个父类,查找顺序:从左到右
#     pass

# start = Xing()

# start.Am()  # i am from Pai (找到的是最左边的)




# class Bar1(object):
#     def Foo1(self):
#         print("i am Bar1_Foo1")

#     def Foo2(self):
#         print("i am Bar1_Foo2")
#         self.Foo1()  ###

# class Bar2(Bar1):
#     def Foo1(self):
#         print("i am Bar2_Foo1")

# obj = Bar2()
# obj.Foo2()



# print(Bar1.__base__)  # <class 'object'>
'''输出
i am Bar1_Foo2   (对象自己没有到父类去找)
i am Bar2_Foo1   (执行到"self.Foo1()"后又返回来从最开始找)
'''


# class Default:
#     pass

# obj=Default()
# print(Default.__base__)  # <class 'object'>






# class People:
#     school = "蟹煲王餐厅"

#     def __init__(self,name,age,sex):
#         self.name = name
#         self.age = age
#         self.sex = sex

# class Staff(People):
#     def sell(self):
#         print(f"{self.name}正在卖蟹煲")
#         # print('%s正在卖蟹煲' %(self.name))

# class Boss(People):
#     def payoff(self,obj,money):
#         print(f"{self.name}给{obj.name}发了{money}元工资")
#         obj.money = money



# S1 = Staff('海绵宝宝', 18, 'male')
# B1 = Boss('蟹老板', 20, 'female')


# S1.sell()  # 海绵宝宝正在卖蟹煲

# B1.payoff(S1, 300)  # 蟹老板给海绵宝宝发了300元工资
# print(S1.money)  # 300

# 继承是一种创建新类的方式，在Python中，新建的类可以继承一个或多个父类，新建的类可称为子类或派生类，父类又可称为基类或超类


# class Parent1():
#     x = 111

# class Parent2():
#     pass

# class Sub1(Parent1):  # 单继承
#     pass

# class Sub2(Parent1,Parent2):  # 多继承
#     pass

# print(Sub1.__bases__)
# print(Sub2.__bases__)
# print(Sub1.x)
# 输出：
# (<class '__main__.Parent1'>,)
# (<class '__main__.Parent1'>, <class '__main__.Parent2'>)
# 111

# ps1: 在python2中有新式类与经典类之分
# 新式类： 继承了object类中子类，以及该类的子类子子类
# 经典类：没有继承object类中子类，以及该类的子类子子类


# 2.为何要有继承： 用来解决类与类之间的冗余问题

# 3. 如何实现继承
# 示范1
# class Student():
#     school = "OLDBOY"

#     def __init__(self,name,age,sex):
#         self.name=name
#         self.age=age
#         self.sex=sex

#     def choose_course(self):
#         print('学生 %s 正在选课' %self.name)
    
# class Teacher():
#     school = "OLDBOY"

#     def __init__(self,name,age,sex,salary,level):
#         self.name=name
#         self.age=age
#         self.sex=sex
#         self.salary=salary
#         self.level=level

#     def course(self):
#         print('老师 %s 老师正在给学生打分' %self.name)

# 示范2: 基于继承类与类之间存在冗余问题

class OldboyPeople():
    school = "OLDBOY"
 
    def __init__(self,name,age,sex):
        self.name=name
        self.age=age
        self.sex=sex

    def score(self):
        print('我只是为了测试父类的函数，通过类.函数的方法去调用')


class Student(OldboyPeople):
    # 可以删掉了
    # school = "OLDBOY"

    # def __init__(self,name,age,sex):
    #     self.name=name
    #     self.age=age
    #     self.sex=sex

    def choose_course(self):
        print('学生 %s 正在选课' %self.name)
    
class Teacher(OldboyPeople):
    # school = "OLDBOY"

    def __init__(self,name,age,sex,salary,level):
        # 这三行就是父类的init方法，删除掉，在这里调用父类的init方法
        # self.name=name
        # self.age=age
        # self.sex=sex
        # 指名道姓去跟OldboyPeople 要__init__方法，类.__init__ 就没有自动传值的说法，有几个参数传几个参数
        OldboyPeople.__init__(self,name,age,sex)
        self.salary=salary
        self.level=level

    def course(self):
        OldboyPeople.score(self)  # 同理使用类.函数()  去调用父类的方法
        print('老师 %s 老师正在给学生打分' %self.name)



# stu_obj=Student('lili',18,'male')
# print(stu_obj.__dict__)  # {'name': 'lili', 'age': 18, 'sex': 'male'}
# print(stu_obj.school)  # OLDBOY
# stu_obj.choose_course()  # 学生 lili 正在选课


teac_obj=Teacher('egon',18, 'female',3000,10)
print(teac_obj.__dict__)
print(teac_obj.school)
teac_obj.course()

# 输出：
# {'name': 'egon', 'age': 18, 'sex': 'female', 'salary': 3000, 'level': 10}
# OLDBOY
# 我只是为了测试父类的函数，通过类.函数的方法去调用
# 老师 egon 老师正在给学生打分

# 派生的三种：
# 把父类的东西拿过来，重名
# 造一个父类没有的
# 把父类的东西拿过来，自己改一改
# 存在重名的就以自己为准


