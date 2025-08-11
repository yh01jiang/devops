class School:  
    school_name = "OLDBOY"  
  
    def __init__(self, nickname, addr):  
        self.nickname = nickname  
        self.addr = addr  
        self.classes = []  
  
    def related_class(self, class_obj):  
        self.classes.append(class_obj)  
  
    def tell_class(self):  
        print(f"{self.nickname} ({self.addr})")  # 先打印学校信息  
        for class_obj in self.classes:  
            class_obj.tell_course()  
  
  
class Class:  
    def __init__(self, name):  
        self.name = name  
        self.course = None  
  
    def related_course(self, course_name):  
        self.course = course_name  
  
    def tell_course(self):  
        print(f"{self.name} - {self.course}")  # 打印班级名称和课程  
  
# 创建学校和班级对象  
school_obj1 = School('老男孩魔都校区', '上海')  
class_obj1 = Class('脱产14期')  
class_obj2 = Class('脱产15期')  
  
# 为班级关联课程并添加到学校  
class_obj1.related_course('python全栈开发')  
class_obj2.related_course('linux运维')  
school_obj1.related_class(class_obj1)  
school_obj1.related_class(class_obj2)  
  
# 调用 tell_class 方法打印学校信息及其包含的班级和课程  
school_obj1.tell_class()
