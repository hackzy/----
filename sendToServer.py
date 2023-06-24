from recBuffer import 读封包
from bufferWrit import 写封包
from threading import  Thread
from saveData import 存档
from setting import *
class 客户请求处理:
    def __init__(self,user,server) -> None:
        self.user = user
        self.server = server

    def 喊话(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        频道 = 读.读短整数型(True)
        读.跳过(5)
        内容 = 读.读文本型()
        内容 = 内容[8:]
        if 内容 == "LZKS":
            self.user.fuzhu.luzhi.录制开始()
            return
        if 内容 == 'LZTZ':
            self.user.fuzhu.luzhi.录制停止()
            return
        if 内容 == 'LZFSKS':
            self.user.fuzhu.luzhi.发送开始()
            return
        if 内容 == 'LZFSTZ':
            self.user.fuzhu.luzhi.发送停止()
            return
        if 内容.find('SZLZYS') != -1:
            self.user.fuzhu.luzhi.设置延时(内容)
            return
        if 内容 == 'LZFS':
            self.user.fuzhu.luzhi.单次发送()
            return
        return buffer
    
    def NPC对话点击处理(self,buffer):
        解包 = self.取对话内容(buffer)
        npcid = 解包[0]
        内容 = 解包[1]
        if npcid == 1:
            self.user.fuzhu.小助手.助手处理中心(内容)
        elif npcid == 2:
            self.user.fuzhu.小助手.助手_自动战斗(内容)
        elif npcid == 3:
            self.user.fuzhu.小助手.装备相关(内容)


    def 取对话内容(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        npcid = 读.读整数型(True)
        内容 = 读.读文本型()
        填写内容 = 读.读文本型()
        返回卡密 = 填写内容
        if 填写内容.find('money:') != -1:
            填写内容 = int(填写内容.split('money:0,')[1].split(':')[0])
        else:
            if 填写内容 != '':
                try:
                    填写内容 = int(填写内容)
                except:
                    填写内容 = 0
        return [npcid,内容,填写内容,返回卡密]
    
    def 选择角色(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        昵称 = 读.读文本型()
        for a in self.user.gamedata.所有角色:
            if self.user.gamedata.所有角色[a]['名称'] == 昵称:
                self.user.gamedata.GID = self.user.gamedata.所有角色[a]['GID']
                self.server.写日志('玩家：'+ 昵称 + ' 上线 ip:'+self.user.客户IP+'  当前在线人数:'+str(len(self.server.user)))
                break

    def 取账号(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        self.user.账号 = 读.读文本型()
        存档.读取存档信息(self.user)
        if self.user.账号 == GM账号:
            self.server.GM.GMUSER = self.user
            self.server.写日志('GM号已上线,现在可执行GM操作')
            t = Thread(target=self.server.GM.检查元宝)
            t.daemon = True
            t.start()

