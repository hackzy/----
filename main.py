from setting import *
from server import Server
from xyplugin import 逍遥插件
import time
import os
'''
***********************《逍遥插件》***************************
**欢迎使用更铸辉煌逍遥插件，作者：hackzy，技术交流QQ：959683906**
** 当前服务器已运行：{}     当前在线人数：{}                  **
*************************************************************
** 菜单*******************************************************
** 1、查询所有在线玩家昵称                                   **
** 2、发送测试封包                                           **
** 3、待添加                                                **
**************************************************************
'''
菜单 = '***************************《逍遥插件》****************************\n\
** 欢迎使用更铸辉煌逍遥插件，作者：hackzy，技术交流QQ：959683906 **\n\
** 当前服务器已运行：{}          当前在线人数：{}           **\n\
*******************************************************************\n\
** 菜单 ***********************************************************\n\
**      1、查询所有在线玩家昵称                                  **\n\
**      2、发送测试封包                                          **\n\
**      3、待添加                                                **\n\
*******************************************************************'


if __name__== '__main__':
    '服务器启动'
    startime = time.time()
    server = 逍遥插件() #创建全局对象
    for sid in range(len(服务器监听端口)):           #根据线路数量创建服务端，一个线路一个服务端
        server.server.append(Server(server))  #创建服务器对象
        server.server[sid].启动服务器(游戏IP,游戏端口[sid],服务器监听地址,服务器监听端口[sid]) #初始化并创建服务端
    while True:
        #print(菜单.format(time.strftime("%H:%M:%S",time.gmtime(time.time()-startime)),len(server.user)))
        #threading.Event().wait(1)
        m = input()
        server.服务器发送(m,server.GM.GMUSER)
        
