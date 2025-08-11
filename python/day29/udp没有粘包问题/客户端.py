import socket

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)




client.sendto(b'hello', ('127.0.0.1', 8090))
client.sendto(b'world', ('127.0.0.1', 8090))

client.close()