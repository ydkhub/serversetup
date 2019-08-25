from socket import *
import threading

# IP = '172.16.0.15'
# IP = '192.168.43.72'
IP = '172.20.10.9'
PORT = 8888
# PORT = 8880

server = socket(AF_INET,SOCK_STREAM)
server.bind((IP,PORT))
server.listen(5)
users = {}
class User:
    def __init__(self,name,sock):
        self.name = name
        self.sock = sock
    def getName(self):
        return self.name
def chat(user,msg):
    if msg.startswith('To:'):
        msgs = msg.split('@')
        other = msgs[0]
        if other[3:] in users:
            # users.get(other[3:]).sock.send(bytes(user.getName()+":"+msgs[1],encoding='utf8'))
            users.get(other[3:]).sock.send(bytes(msgs[1],encoding='utf8'))
            print(user.getName()+"--->"+other+":\n"+msgs[1])
        else:
            user.sock.send(bytes('此用户没有上线',encoding='utf8'))
    else:
        pass
        # user.sock.send(bytes('输入格式错误',encoding='utf8'))
def connectThread(name,sock):
    while True:
        try:
            user = User(name,sock)
            if name not in users:
                users[name] = user
            mchat = threading.Thread(target=chat, args=(user, str(sock.recv(1024),encoding='utf8')))
            # chat(user,)
            mchat.start()
        except ConnectionResetError:
            print(user.getName()+'退出')
            del users[name]
            sock.close()
            break


if __name__ == '__main__':
    import time
    while True:
        print("等待用户连接")
        sock,addr = server.accept()
        # sock.send(bytes("连接成功",encoding='utf8'))
        print(addr)
        # sock.send(bytes("连接成功,欢迎你",encoding="utf8"))
        name = str(sock.recv(1024),encoding='utf8')[0:7]
        name = name.strip()
        print(len(name))
        print(name)
        con = threading.Thread(target=connectThread,args=(name,sock))
        con.start()
