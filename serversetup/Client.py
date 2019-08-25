__author__ = "liyanhong"
from socket import *
import threading

# IP = '192.168.43.72'
IP = '172.20.10.9'
# IP='111.231.232.211'
# IP='10.100.178.104'
# PORT = 6066
PORT = 8888
def Recv(sock,test):
    while True:
        try:
            data = str(sock.recv(1024),encoding='utf8')
            print("\t\t\t\t\t\t%s"%data)
        except ConnectionResetError:
            sock.close()
            print("服务器关闭或者被强制下线")
            threading.Event()
            break
def Send(sock,test):
    while True:
        try:
            other = input("请输入你想和谁聊天-->")
            data = input("内容:")
            sock.send(bytes("To:%s%s%s"%(other,"@",data),encoding='utf8'))
            sock.send(bytes(data,encoding='utf8'))
        except (OSError,ConnectionResetError):
            sock.close()
            print("服务器关闭或者被强制下线,按照任意键退出")
            threading.Event()
            break

if __name__ == '__main__':
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((IP, PORT))
        # while True:
        data = input('请您的输入名字-->')
        client.send(bytes(data,encoding='utf8'))
        # while True:
            # data = input('内容')
            # client.send(bytes(data,encoding='utf8'))

        recv = threading.Thread(target=Recv,args=(client,None))
        send = threading.Thread(target=Send,args=(client,None))
        recv.start()
        send.start()
        recv.join()
        send.join()
    except (ConnectionResetError,ConnectionRefusedError):
        print("服务器未开启")
