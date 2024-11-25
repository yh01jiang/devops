# r只读模式: 在文件不存在时则报错,文件存在文件内指针直接跳到文件开头

# with open(r'a.txt',mode='rt',encoding='utf-8') as f:
#      res=f.read() # 会将文件的内容由硬盘全部读入内存，赋值给res

# # print(res)



# with open('a.txt',mode='rt',encoding='utf-8') as f:
#     for line in f:
#         print(line) # 同一时刻只读入一行内容到内存中




# # 小练习：实现用户认证功能
#  inp_name=input('请输入你的名字: ').strip()
#  inp_pwd=input('请输入你的密码: ').strip()
#  with open(r'db.txt',mode='r',encoding='utf-8') as f:
#      for line in f:
#          # 把用户输入的名字与密码与读出内容做比对(解压赋值)
#          u,p=line.strip('\n').split(':')
#          if inp_name == u and inp_pwd == p:
#              print('登录成功')
#              break
#      else:
#          print('账号名或者密码错误')、






with open('a.txt','r') as read_f,open('b.txt','w') as write_f:  
    data = read_f.read()
    write_f.write(data)