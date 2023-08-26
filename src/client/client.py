import socket
from setting import *
from threading import Timer,Thread as 线程
import traceback
from src.game.GameData import GameData
from src.assisted.fuzhu import fuzhu
from .sendToClient import SendToClient

class Client:
    '''客户对象类，每个客户连接插件服务端就创建一个客户对象连接游戏的服务器'''
    def __init__(self,server) -> None:
        '''初始化客户属性'''
        self.server = server
        self.未请求 = b''
        self.gamedata = GameData()
        self.fuzhu = fuzhu(server,self)
        self.账号 = ''
        self.在线中 = False
        self.未发送 = b''
        self.time = 0
    def 客户端启动(self,ip,端口):
        '''启动连接服务器'''
        try:
            self.服务器句柄 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.服务器句柄.connect((ip,端口))
            self.server.cThreads.submit(self.数据到达)
            '''c1 = 线程(target=self.数据到达)
            c1.setDaemon(True)
            c1.start()'''
        except:
            self.server.写日志("连接服务器失败，请检查服务器是否开启，详细错误：{}".format(traceback.format_exc()))

    def 初始化客户信息(self,客户句柄:socket.socket,客户IP:str,cid:int):
        '''初始化客户连接属性'''
        self.客户句柄 = 客户句柄
        self.客户IP = 客户IP
        self.cid = cid
        self.在线中 = True

    def 数据到达(self):
        '''开始接收服务器发来的数据'''
        while True:
            try:
                buffer = self.服务器句柄.recv(20000)
                if buffer == b'' :
                        # 删除连接
                    if self.账号 == GM账号:
                        self.server.写日志('GM号已掉线,所有功能已失效')
                        self.server.GM.GMUSER = None
                        self.server.GM.挂载 = False
                    self.server.删除客户(self)
                    return
                else:
                    self.server.tlock.acquire()
                    self.未发送 += buffer
                    self.server.tlock.release()
                    self.server.cThreads.submit(self.接收处理线程)
            except:
                self.server.删除客户(self)
                return

    def 接收处理线程(self):
        self.server.tlock.acquire()
        while self.未发送[:2] == b'MZ':
            leng = int.from_bytes(self.未发送[8:10])
            if len(self.未发送) - 10 >= leng:
                buffer = self.未发送[:leng+10]
                self.未发送 = self.未发送[leng + 10:]
                self.接收处理中心(buffer)
                continue
            break
        self.server.tlock.release()
    def 接收处理中心(self,buffer:bytes):
        客户接收处理 = SendToClient(self,self.server)
        包头 = buffer[10:12]
        if 包头.hex() == "3357":
            buffer = 客户接收处理.登录线路(buffer)
        elif 包头.hex() == "4355":
            buffer = 客户接收处理.显示线路(buffer)
        elif 包头.hex() == '5009':
            buffer = 客户接收处理.切换角色(buffer)
        elif 包头.hex() == '5103':
            客户接收处理.背包读取(buffer)
        elif 包头.hex() == '203d' or 包头.hex() == '39f1':
            客户接收处理.人物属性读取(buffer)
        elif 包头.hex() == '2821':
            客户接收处理.技能读取(buffer)
        elif 包头.hex() == '7103':
            #屏蔽垃圾
            if self.gamedata.屏蔽垃圾:
                buffer = b''
        elif 包头.hex() == 'f05d':
                客户接收处理.周围对象读取(buffer)
        elif 包头.hex() == '226f':
                self.gamedata.参战宠物id = int.from_bytes(buffer[12:16])
        elif 包头.hex() == '5203':
            if buffer[19:20].hex() == '19':
                if self.fuzhu.自动战斗.开关:
                    buffer = self.server.基础功能.战斗时间(buffer)
                    t1 = Timer(4,self.fuzhu.自动战斗.开始战斗)
                    t1.start()
        elif 包头.hex() == '1de5':
            if self.fuzhu.自动战斗.开关:
                self.fuzhu.自动战斗.置攻击位置id(buffer)
        elif 包头.hex() == '10dd':
            if self.fuzhu.自动战斗.开关:
                self.fuzhu.自动战斗.删攻击id(buffer)
        elif 包头.hex() == '1155':
            客户接收处理.地图事件(buffer)
        elif 包头.hex() == 'f061':
            客户接收处理.取角色gid(buffer)
        elif 包头.hex() == '1101' and self == self.server.GM.GMUSER:
            self.server.GM.元宝寄售(buffer)
        elif 包头.hex() == '1a29':
            客户接收处理.战斗对话(buffer)
        elif 包头.hex() == 'fd67':
            客户接收处理.商城读取(buffer)
        elif 包头.hex() == '2037':
            buffer = 客户接收处理.NPC对话(buffer)
        elif 包头.hex() == 'f0b3':
            客户接收处理.宠物数据更新(buffer)
        elif 包头.hex() == '20cf':
            客户接收处理.宠物读取(buffer)
        elif 包头.hex() == '0dfd':
            if self.fuzhu.自动战斗.开关:
                t = 线程(target=self.fuzhu.自动战斗.补充状态())
                t.start()
        elif 包头.hex() == '1393':
            客户接收处理.读当前坐标(buffer)
        elif 包头.hex() == 'f0dd':
            客户接收处理.读自身显示属性(buffer)
        elif 包头.hex() == '2603':
            客户接收处理.任务读取(buffer)
        elif 包头.hex() == 'f9c3' and self.账号 == GM账号 and self.server.GM.挂载:
            self.server.GM.setHeartbeatd(buffer)
            buffer = b''

        try:
            if len(buffer) != 0 and self.客户句柄 != 0:
                self.客户句柄.send(buffer)
        except:
            self.客户句柄.close()
