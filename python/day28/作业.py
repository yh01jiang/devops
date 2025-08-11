# 整合--》解耦合-->方便扩展

class School:
    school_name="OLDBOY"
    
    def __init__(self,nickname,addr):
        self.nickname=nickname
        self.addr=addr
        self.classes=[]

    def related_class(self,class_obj):
        # self.classes.append(班级名字)
        self.classes.append(class_obj)

    def tell_class(self):
        for class_obj in self.classes:
            class_obj.tell_course()
# 一 学校
# # 1. 创建校区
school_obj1=School('老男孩魔都校区', '上海')
school_obj2=School('老男孩帝都校区', '北京')

# # 2. 为学校开设班级

# #上海校区开设python 脱产14 15 期
# school_obj1.related_class('脱产14期')
# school_obj1.related_class('脱产15期')
# # print(school_obj1.classes)
# # 北京校区开设脱产29期
# school_obj2.related_class('脱产29期')
# # print(school_obj2.classes)


# # for class_name in school_obj1.classes:
# #     print('%s %s' %(school_obj1.nickname,class_name))

# # for class_name in school_obj2.classes:
# #     print('%s %s' %(school_obj2.nickname,class_name))

# # 3. 查看每个校区开设的班级

# school_obj1.tell_class()
# school_obj2.tell_class()



# print(school_obj1.school_name)
# print(school_obj1.nickname)
# print(school_obj1.addr)

# 二 班级

class Class:
    def __init__(self,name):
        self.name=name
        self.course = None

    def related_course(self, course_name):
        self.course=course_name

    def tell_course(self):
        print('%s %s' %(self.name, self.course))

# 1. 创建班级
class_obj1=Class('脱产14期')
class_obj2=Class('脱产15期')
class_obj3=Class('脱产29期')

#2. 为班级关联课程
class_obj1.related_course('python全栈开发')
class_obj2.related_course('linux运维')
class_obj3.related_course('python全栈开发')

#3. 查看班级开设的课程
# class_obj1.tell_course()
# class_obj2.tell_course()
# class_obj3.tell_course()

#4. 为学校开设班级
#上海校区开设python 脱产14 15 期
school_obj1.related_class(class_obj1)
school_obj1.related_class(class_obj2)
#北京校区开设脱产29期
school_obj2.related_class(class_obj3)

# print(school_obj1.classes)
# print(class_obj1.name)

school_obj1.tell_class()

# school_obj2.tell_class()



class Course:
    pass





