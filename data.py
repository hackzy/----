from setting import *


class 数据池 :
    '''数据管理，检查收到的数据是否完整'''
    def __init__(self) -> None:
        self.data = []
        self.now = 0

    def 置数据(self,buffer):
        self.data = buffer.split(组包包头)
        print(self.data)
        self.now = 0

    def 取出数据(self):
        if self.now > len(self.data) -1:
            self.now += 1
            return 组包包头 + self.data[0]
        if self.data[self.now] == b"":
            self.now += 1
        leng = int.from_bytes(self.data[self.now][:2],'big')
        if len(self.data[self.now]) - 2 == leng:
            buffer = 组包包头 + self.data[self.now]
            self.now += 1
            return buffer
        buffer = 组包包头 + self.data[self.now]
        self.now += 1
        return buffer
    def 是否还有剩余(self):
        if self.now <= len(self.data) - 1:
            return True
        return False