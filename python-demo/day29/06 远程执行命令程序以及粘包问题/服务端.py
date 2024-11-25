
import subprocess
import struct
from socket import *
server=socket(AF_INET,SOCK_STREAM)
server.bind(('127.0.0.1', 8089))
server.listen(5)

# 服务端需要做的两件事
# 第一件事.： 循环的从从半链接池取出链接请求与其建立双向链接，拿到链接对象。
while True:
    conn, client_addr=server.accept()
    print(conn, client_addr)

    # 第二件事： 拿到链接对象，请求进行通信循环
    while True:
        try:
            cmd=conn.recv(1024)
            if len(cmd) == 0:
                break
            print(cmd.decode('utf-8'))
            obj=subprocess.Popen(cmd.decode('utf-8'),
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             )
            stdout_res=obj.stdout.read()
            stderr_res=obj.stderr.read()
            total_size=(len(stderr_res)+len(stdout_res))
            # conn.send(stdout_res+stderr_res)  # 等同于如下
            # 1） 先发头部信息（固定长度的bytes）： 对数据描述信息
            # int --> 固定长度的bytes
            header=struct.pack('i',total_size)
            conn.send(header)

            # 2) 再发真实的数据
            conn.send(stdout_res)
            conn.send(stderr_res)

        except Exception:
            break
    conn.close()