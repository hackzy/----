import socket
from setting import *
from threading import Thread as 线程
from clientData import 客户端数据处理
import traceback
class Client:
    '''客户对象类，每个客户连接插件服务端就创建一个客户对象连接游戏的服务器'''
    def __init__(self,server) -> None:
        '''初始化客户属性'''
        self.cid = 0
        self.客户IP = 0
        self.server = server
        self.sid = 0
        self.客户句柄 = 0
        self.服务器句柄 = 0
        self.使用中 = False
        self.客户数据处理 = 客户端数据处理(self.server)
        self.未请求 = bytes()
    
    def 客户端启动(self,ip,端口):
        '''启动连接服务器'''
        try:
            self.服务器句柄 = socket.socket()
            self.服务器句柄.connect((ip,端口))
            c1 = 线程(target=self.数据到达)
            c1.setDaemon(True)
            c1.start()
        except:
            self.server.写日志("连接服务器失败，请检查服务器是否开启，详细错误：{}".format(traceback.format_exc()))
    def 初始化客户信息(self,cid,客户句柄,客户IP,sid):
        '''初始化客户连接属性'''
        self.cid = cid
        self.客户句柄 = 客户句柄
        self.客户IP = 客户IP
        self.sid = sid
    
    def 数据到达(self):
        '''开始接收服务器发来的数据'''
        while True:
            try:
                if self.服务器句柄 != -1:
                    buffer = self.服务器句柄.recv(100000)
                    if len(buffer) == 0:
                        self.服务器句柄.close()
                        # 删除连接
                        print("断开与服务器连接",self.服务器句柄,self.cid)
                        break
                    self.客户数据处理.未发送 += buffer
                    self.客户数据处理.接收处理线程(self.cid)

            except:
                print("接收数据异常",len(buffer),traceback.format_exc())
