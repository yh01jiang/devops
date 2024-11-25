# import sys #导入模块

# x=1 #定义全局变量,如果非必须,则最好使用局部变量,这样可以提高代码的易维护性,并且可以节省内存提高性能

# class Foo: #定义类,并写好类的注释
#     'Class Foo is used to...'
#     pass

# def test(): #定义函数,并写好函数的注释
#     'Function test is used to…'
#     print('我是python脚本')

# if __name__ == '__main__': #主程序
#     test() #在被当做脚本执行时,执行此处的代码
# else:
#     print('我是一个模块哦')



class Student:
    # 1、变量的定义
    stu_school='oldboy'
    count=0

    # __init__在类调用阶段自动触发
    # 空对象, 'egon', 20, 'male'
    def __init__(self,x,y,z):
        Student.count+=1  # 每实例化一次加1
        self.stu_name=x   # 空对象.stu_name='egon'
        self.stu_age=y    # 空对象.stu_age=20
        self.stu_gender=z # 空对象.stu_gender='male'

    # 2、功能的定义
    def tell_stu_info(self):
        print('名字：%s 年龄： %d 性别： %s' %(
            self.stu_name, 
            self.stu_age, 
            self.stu_gender
        ))


    def set_info(self,x,y,z):
        self.stu_name=x
        self.stu_age=y
        self.stu_gender=z

    # obj 用来接收绑定方法调用时自动传入那个对象，标准是self
    # 但凡在类中定义的函数，就必须有一个固定的参数self
    def choose(self,x):
        print('正在选课')
        self.course=x




stu1_obj=Student('egon', 20, 'male')  # 只要你调用类了，就会自动把空对象传进去，Student.__init__(空对象, 'egon', 20, 'male')，你只需要在括号内传入其他参数即可
stu2_obj=Student('lili', 30, 'female')
stu3_obj=Student('tom', 40, 'male')

# 实例化一次就加1
# print(stu1_obj.count)
# print(stu2_obj.count)
# print(stu3_obj.count)

# # # 属性查找，先从对象里面查找，再从类里面查找
# print(stu1_obj.stu_name) # egon
# print(stu1_obj.stu_age)  # 20
# print(stu1_obj.stu_gender) # male
# print(stu1_obj.stu_school)  # oldboy


# # 类中存放的是对象共有的数据与功能
# # 一、类可以访问: 
# # 1、类的数据属性
# # 2、类的函数属性
# print(Student.stu_school)
# print(Student.tell_stu_info)
# print(Student.set_info)
# 输出
# oldboy
# <function Student.tell_stu_info at 0x104a8caf0>
# <function Student.set_info at 0x104a8cb80>

# # 二、但其实类中的东西是给对象使用的
# # 1、类的数据属性是共享给所有对象使用的，大家访问的地址都一样

# print(id(Student.stu_school))
# print(id(stu1_obj.stu_school))
# print(id(stu2_obj.stu_school))
# print(id(stu3_obj.stu_school))

# # # 输出：
# # 4369059952
# # 4369059952
# # 4369059952
# # 4369059952

# # 修改类中的值，所有对象的值都会发生改变
# Student.stu_school='OLDBOY'  
# print(Student.stu_school)
# print(stu1_obj.stu_school)
# print(stu2_obj.stu_school)
# print(stu3_obj.stu_school)

# # 输出
# # OLDBOY
# # OLDBOY
# # OLDBOY
# # OLDBOY
# # 修改某一个对象的值，只有指定的对象值发生改变，其余对象以及类不发生改变。
# stu1_obj.stu_school='OLDBOY' 
# print(Student.stu_school)
# print(stu1_obj.stu_school)
# print(stu2_obj.stu_school)
# print(stu3_obj.stu_school)
# # 输出
# # OLDBOY
# # OLDBOY
# # OLDBOY
# # OLDBOY

# # 2、类的函数属性是绑定给对象使用的,而且是绑定给对象的，虽然所有对象指向的都是相同的功能，但是绑定到不同的对象就是不同的绑定方法，内存地址各不相同
# # 其实类调用自己的函数也是可以使用的，严格按照函数的规则进行使用。函数有几个参数，调用就需要几个参数
# print(Student.tell_stu_info)
# print(Student.set_info)

# 输出
# <function Student.tell_stu_info at 0x100a70c10>
# <function Student.set_info at 0x100a70ca0>

# Student.tell_stu_info(stu1_obj)
# Student.tell_stu_info(stu2_obj)
# Student.tell_stu_info(stu3_obj)

# # 输出
# # 名字：egon 年龄： 20 性别： male
# # 名字：lili 年龄： 30 性别： female
# # 名字：tom 年龄： 40 性别： male

# Student.set_info(stu1_obj, 'EGON', 21, 'female')
# Student.tell_stu_info(stu1_obj) # 名字：EGON 年龄： 21 性别： female

# # 绑定方法的特殊之处：谁来调用绑定方法就会将谁当做第一个参数自动传入
# print(Student.tell_stu_info)
# print(stu1_obj.tell_stu_info)
# print(stu2_obj.tell_stu_info)
# print(stu3_obj.tell_stu_info)

# #输出：
# # <function Student.tell_stu_info at 0x104cd09d0>
# # <bound method Student.tell_stu_info of <__main__.Student object at 0x104cdcf40>>
# # <bound method Student.tell_stu_info of <__main__.Student object at 0x104cdce80>>
# # <bound method Student.tell_stu_info of <__main__.Student object at 0x104cdcd60>>


# stu1_obj.tell_stu_info() # 等同于tell_stu_info(stu1_obj)
# stu2_obj.tell_stu_info() # 等同于tell_stu_info(stu2_obj)
# stu3_obj.tell_stu_info() # 等同于tell_stu_info(stu3_obj)

# Student.tell_stu_info(stu1_obj) # 名字：egon 年龄： 20 性别： male
# # 输出：
# 名字：egon 年龄： 20 性别： male
# 名字：lili 年龄： 30 性别： female
# 名字：tom 年龄： 40 性别： male

# # 注意：绑定到对象方法的这种自动传值的特征，决定了在类中定义的函数都要默认写一个参数self，self可以是任意名字，但命名为self是约定俗成的。
# stu1_obj.choose('python全栈开发')
# print(stu1_obj.course)

# stu2_obj.choose('linux运维')
# print(stu2_obj.course)

# stu3_obj.choose('高级架构师')
# print(stu3_obj.course)

# # 输出：
# 正在选课
# python全栈开发
# 正在选课
# linux运维
# 正在选课
# 高级架构师