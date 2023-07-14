from luzhi import Luzhi
from autoFired import 自动战斗
from xiaozhushou import XiaoZhuShou
from bufferWrit import 写封包
from setting import *
from threading import Event,Thread
import random
class fuzhu:
    def __init__(self,server,user) -> None:
        self.luzhi = Luzhi(server,user)
        self.自动战斗 = 自动战斗(server,user)
        self.小助手 = XiaoZhuShou(server,user)
        self.鉴定类型 = ''
        self.user = user
        self.server = server
        self.开始改造 = False
        self.改造类型 = ''

    def 血蓝位置(self):
        法玲珑 = 0
        血玲珑 = 0
        驯兽诀 = False
        for a in self.user.gamedata.物品数据:
            if self.user.gamedata.物品数据[a].名称.find('法玲瓏') != -1:
                法玲珑 = a
            if self.user.gamedata.物品数据[a].名称.find('血玲瓏') != -1:
                血玲珑 = a
            if self.user.gamedata.物品数据[a].名称.find('馴獸訣') != -1:
                驯兽诀 = True
        if 法玲珑 == 0:
            self.server.基础功能.商城购买道具(self.user,'特級法玲瓏')
            for a in self.user.gamedata.物品数据:
                if self.user.gamedata.物品数据[a].名称.find('法玲瓏') != -1:
                    法玲珑 = a
        if 血玲珑 == 0:
            self.server.基础功能.商城购买道具(self.user,'特級血玲瓏')
            for a in self.user.gamedata.物品数据:
                if self.user.gamedata.物品数据[a].名称.find('血玲瓏') != -1:
                    血玲珑 = a
        if 驯兽诀 == False:
            self.server.基础功能.商城购买道具(user = self.user,道具 = '高級馴獸訣')
        return 血玲珑,法玲珑
    
    def 人物回复(self,血玲珑,法玲珑):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('202c'))
        写.写字节型(法玲珑.to_bytes(1))
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        写 = 写封包()
        写.写字节集(bytes.fromhex('202c'))
        写.写字节型(血玲珑.to_bytes(1))
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        for a in range(3):
            self.server.客户端发送(完整包.取数据(),self.user)
            #print(self.user.gamedata.最大气血,self.user.gamedata.最大法力)
    def 宠物回复(self,血玲珑,法玲珑):
        try:
            写 = 写封包()
            完整包 = 写封包()
            写.写字节集(bytes.fromhex('204e'))
            写.写字节型(self.user.gamedata.pet[self.user.gamedata.参战宠物id].位置.to_bytes(1))
            写.写字节型(血玲珑.to_bytes(1))
            完整包.写字节集(组包包头)
            完整包.写字节集(写.取数据(),True,1)
            写 = 写封包()
            写.写字节集(bytes.fromhex('204e'))
            写.写字节型(self.user.gamedata.pet[self.user.gamedata.参战宠物id].位置.to_bytes(1))
            写.写字节型(法玲珑.to_bytes(1))
            完整包.写字节集(组包包头)
            完整包.写字节集(写.取数据(),True,1)
            if self.user.gamedata.pet[self.user.gamedata.参战宠物id].忠诚 < 80:
                    写 = 写封包()
                    写.写字节集(bytes.fromhex('109a'))
                    写.写整数型(self.user.gamedata.参战宠物id,True)
                    完整包.写字节集(组包包头)
                    完整包.写字节集(写.取数据(),True,1)
            for a in range(3):
                self.server.客户端发送(完整包.取数据(),self.user)
        except:
            return
        
    def 一键鉴定(self):
        if len(self.user.gamedata.物品数据) == 0:
            return
        for back in self.user.gamedata.物品数据:
            if back > 100:
                写 = 写封包()
                写.写字节集(组包包头)
                写.写字节集(bytes.fromhex('0006301c'))
                写.写整数型(back,True)
                self.user.服务器句柄.send(写.取数据())
                Event().wait(timeout=0.2)
        self.鉴定类型 = ''

    def 鉴定二级对话(self,NPCID,对话内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('3038'))
        写.写整数型(NPCID,True)
        if 对话内容.find('花費') != -1:
            写.写文本型('確定',True)
        else:
            写.写文本型(self.鉴定类型,True)
        写.写字节型(b'\x00')
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        self.user.服务器句柄.send(完整包.取数据())
        
    def 装备改造(self):
        item = []
        写 = 写封包()
        完整包 = 写封包()
        if self.改造类型 == '改造武器':
            改造道具 = '超級靈石'
        else:
            改造道具 = '超級晶石'

        for a in self.user.gamedata.物品数据:
            if self.user.gamedata.物品数据[a].名称 == 改造道具:
                item.append(a)
        if len(item) < 6:
            数量 = 6 - len(item)
            self.server.基础功能.商城购买道具(self.user,改造道具,数量=数量)
            Event().wait(0.3)
            for a in self.user.gamedata.物品数据:
                if self.user.gamedata.物品数据[a].名称 == 改造道具:
                    item.append(a)
        if len(item) < 6:
            return
        写.写字节集(bytes.fromhex('508A'))
        写.写整数型(self.user.gamedata.角色id,True)
        写.写短整数型(1,True)
        写.写短整数型(7,True)
        写.写整数型(101,True)
        for b in range(6):
            写.写整数型(item[b],True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()

    def 改造线程(self):
        while self.开始改造:
            self.server.客户端发送(self.装备改造(),self.user)
            Event().wait(0.3)

'''    def 自动遇怪(self):
        
        swall = 写封包()
        swrite.写字节集(bytes.fromhex('F0C2'))
        swrite.写整数型(self.user.gamedata.角色id,True)
        swrite.写整数型(self.user.gamedata.当前地图[0],True)
        swrite.写短整数型(5,True)
        for i in range(5):
            x,y = random.randint(-1,1),random.randint(-1,1)
            if x == 0 and y == 0:
                x == 1
            x += self.user.gamedata.当前坐标[0]
            y += self.user.gamedata.当前坐标[1]
            swrite.写短整数型(x,True)
            swrite.写短整数型(y,True)
            self.user.gamedata.当前坐标[0] = x
            self.user.gamedata.当前坐标[1] = y
        ck = random.randint(1,5)
        swrite.写短整数型(ck,True)
        swrite.写整数型(0,True)
        swall.写字节集(组包包头)
        swall.写字节集(swrite.取数据(),True,1)
        self.server.客户端发送(swall.取数据(),self.user)
        print(swall.取数据().hex())
        cwrite = 写封包()
        cwall = 写封包()
        cwrite.写字节集(bytes.fromhex('402F'))
        cwrite.写整数型(self.user.gamedata.角色id,True)
        cwrite.写短整数型(self.user.gamedata.当前坐标[0],True)
        cwrite.写短整数型(self.user.gamedata.当前坐标[1],True)
        cwrite.写短整数型(ck,True)
        cwall.写字节集(组包包头)
        cwall.写字节集(cwrite.取数据(),True,1)
        self.server.服务器发送(cwall.取数据(),self.user)
        print(cwall.取数据().hex())
        print('遇怪封包')

    def 自动遇怪线程(self):
        print('遇怪线程启动')
        while self.是否遇怪:
            print('循环遇怪中')
            self.自动遇怪()
            Event().wait(5)'''