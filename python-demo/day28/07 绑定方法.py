# 一 绑定方法： 特殊之处在于将调用者本身当作第一个参数自动传入
#     1. 绑定给对象的方法： 调用者是对象，自动传入的是对象
#     2. 绑定给类的方法：   调用者是类，自动传入的是类

# import settings

# class Mysql:
#     def __init__(self,ip,port):
#         self.ip=ip
#         self.port=port

#     def func(self):
#         print('%s:%s' %(self.ip, self.port))

#     @classmethod  # 将下面的函数装饰城绑定给类的方法
#     def from_conf(cls):  # 是为了把类Mysql写活,cls约定成俗
#         return cls(settings.IP,settings.PORT)


# # obj1=Mysql('1.1.1.1', 3306)


# # 把setting.py 用户配置的ip port 传入到Mysql类中




# # obj2=Mysql(settings.IP,settings.PORT)

# # 应用场景：比较窄
# # 实现自动的从配置文件加载配置
# obj2=Mysql.from_conf()
# print(obj2.__dict__)

# # 输出
# # {'ip': '127.0.0.1', 'port': 3306}




# 二 非绑定方法===》静态方法（谁都可以来调用）
    # 没有绑定给任何人：调用者可以是类，可以是对象，没有自动传参的效果

class Mysql:
    def __init__(self,ip,port):
        self.uuid= self.create_id  # 更进一步直接获取
        self.ip=ip
        self.port=port

    @staticmethod  # 将下述函数装饰成一个静态方法
    def create_id():
        import uuid
        return uuid.uuid4
    
    @classmethod
    def f1(self):
        pass

    def f2(self):
        pass
    
obj1=Mysql('127.0.0.1', 3306)

# print(Mysql.create_id)  # <function Mysql.create_id at 0x1005789d0>
# print(obj1.create_id)   # <function Mysql.create_id at 0x1005789d0>


# Mysql.create_id(1,2,3)  # 1 2 3
# obj1.create_id(4,5,6)   # 4 5 6





print(Mysql.create_id)  # <function Mysql.create_id at 0x104fa89d0>
print(Mysql.f1)         # <bound method Mysql.f1 of <class '__main__.Mysql'>>
print(obj1.f2)          # <bound method Mysql.f2 of <__main__.Mysql object at 0x102a16f10>>


# 类中的三种方法：
# 不加任何装饰的情况下：默认绑定给对象，会将对象自动传入
# 还有一种绑定给类的，调用者是类，将类传入自动传入
# 还有一种非绑定的，调用者可以是类，也可以是对象，调用的时候就是一盒普通函数，该怎么传参就怎么传参

# 类体代码不需要类，也不需要对象，还能运行，并且还需要将此防范在再类体代码中集成，那么就的使用静态非绑定方法
