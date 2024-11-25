# import time
# print(time.time())
# print(time.strftime("%Y-%m-%d %X"))
# print(time.localtime())
# print(time.gmtime())

# print(time.strftime('%Y-%m-%d %H:%M:%S'))
# print(time.strftime('%Y-%m-%d %H:%M:%S %p'))
# print(time.strftime('%Y-%m-%d %X'))

# res=time.localtime()
# print(res)
# print(res.tm_year)
# print(res.tm_yday)

# import datetime
# print(datetime.datetime.now())
# print(datetime.datetime.now() + datetime.timedelta(days=3))
# print(datetime.datetime.now() + datetime.timedelta(days=-3))
# print(datetime.datetime.now() + datetime.timedelta(weeks=1))
# print(datetime.datetime.now() + datetime.timedelta(days=365*3))


import time
# 时间戳转换为结构化时间
res=time.time()
print(time.localtime(res))

# 结构化时间转为格式化时间
res1=time.localtime()
print(time.strftime('%Y-%m-%d %H:%M:%S',res1))

# 结构化时间===》时间戳
res2=time.localtime()
print(time.mktime(res2))

# 格式化时间====》 结构化时间
res3=time.strptime('1988-03-03 11:11:11','%Y-%m-%d %H:%M:%S')
print(res)




# format string ---> struct_time ----> timestamp
struct_time=time.strptime('1988-03-03 11:11:11','%Y-%m-%d %H:%M:%S')
print(struct_time)
timestamp=time.mktime(struct_time)+7*86400
print(timestamp)



#  timestamp  ----> struct_time  ---->  format string
res4=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp))
print(res4)