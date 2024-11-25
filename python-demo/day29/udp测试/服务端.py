import socket

# 1.创建一个套接字，
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 10000))
while True:
    data, address = sock.recvfrom(4096)
    print(data.decode('UTF-8'), address)
    if data:
        sock.sendto('已接收到你发来的消息'.encode('UTF-8'), address)
