# class People:
#     def __init__(self,name,age,gender):
#         self.name=name
#         self.age=age
#         self.gender=gender


# obj=People('egon',18,'male')
# print(obj.__dict__)  # {'name': 'egon', 'age': 18, 'gender': 'male'}

# print(dir(obj))  # 列表中查看到的属性全为字符串
# # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age', 'gender', 'name']

# print(dir(obj)[-2])  # gender

# res=hasattr(obj, 'name')  # 按字符串'name'判断有无属性obj.name
# print(res)  # True

# getattr(obj, 'sex', None)  # 等同于obj.sex,不存在该属性则返回默认值None
# print(getattr(obj, 'sex', None))  # None 

# print(getattr(obj, 'age'))  # 18

# setattr(obj, 'age', 20)  # 等同于obj.age=18

# print(delattr(obj, 'age'))  # # 等同于del obj.age
# # print(getattr(obj, 'age'))




# class Teacher:
#     def __init__(self,full_name):
#         self.full_name =full_name

# t=Teacher('Egon Lin')

# # hasattr(object,'name')
# hasattr(t,'full_name') # 按字符串'full_name'判断有无属性t.full_name
# print(hasattr(t, 'full_name'))  # True

# # # getattr(object, 'name', default=None)
# getattr(t,'full_name',None) # 等同于t.full_name,不存在该属性则返回默认值None
# print(getattr(t,'full_name',None))  # Egon Lin


# # # setattr(x, 'y', v)
# setattr(t,'age',18) # 等同于t.age=18
# print(setattr(t,'age',18))  # None

# print(t.__dict__)  # {'full_name': 'Egon Lin', 'age': 18}

# # # delattr(x, 'y')
# delattr(t,'age') # 等同于del t.age


# print(hasattr(t, 'age'))

# print(getattr(t, 'age'))

# 判断一把
# obj=10
# if hasattr(obj, 'x'):
#     setattr(obj, 'x', 11111)
# else:
#     pass



# 案例
class Ftp:
    def put(self):
        print('正在执行上传功能')
    
    def get(self):
        print('正在执行下载功能')

    # 与用户交互的一个功能
    def interactive(self):
        method=input('>>>: ').strip()  # mothod='put'  因为输入的是字符串，相当于把put赋值给method，但是不能self.method,因为self一般是.属性的，
        if hasattr(self, method):
            getattr(self, method)()
        else:
            print('输入的指令不存在')

obj=Ftp()
obj.interactive()