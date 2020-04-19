from socket import *
import SQLPart
import threading
import SendFile
import os
import struct
from time import *

logRequest = 100 #登录
regRequest = 101 #注册
friRequest = 102 #请求获得好友列表
chatBegin = 104
ok = 666 #成功
#登录失败
fallOfNo = 601 #失败原因：该用户没有注册
fallOfWP = 602 #失败原因：密码错误
#注册失败
fallOfI = 610 #失败原因：用户名非法
fallOfA = 611 #失败原因：用户名已占用
isMes = 850
delFri = 801
addFri = 800
aggFri = 810
disFri = 811
chatFri = 888
insheet = 901 # 失败原因：用户已经在好友列表中
notinsheet = 903 # 失败原因：该用户名未注册
friNotOnline = 103 #好友不在线，无法聊天
fileSend = 1000
picSend = 1001
newsNum = 802 #新消息数目
friOk = 803 #好友申请成功数目
friFall = 804 #好友申请失败数目
friReq = 805 #收到好友申请数目

g_conn_pool = []
usertable = []
Mess = []
serverPort = 12000
buffsize = 1024
tmp_path = '.\\tmpfiles\\'

# 登陆模式
def LogPart(usertable,sock):
    uID = sock.recv(buffsize).decode()
    uPA = sock.recv(buffsize).decode()
    Flag = str(SQLPart.find(usertable,uID,uPA)).encode()
    if Flag.decode() == (str)(ok):
        SQLPart.setOL(True,uID) 
    sock.send(Flag)
    return uID
    
# 注册模式
def RegPart(sock):
    nID = sock.recv(buffsize).decode()
    nPA = sock.recv(buffsize).decode()
    Flag = str(SQLPart.register(nID,nPA)).encode()
    sock.send(Flag)
    return nID

def deletemess(NowID,s,type):
    if NowID == '': return
    for i in range(len(Mess)):
        x = Mess[i].find(NowID)
        f1 = Mess[i].find('From ')
        f2 = Mess[i].find(',FriendReq')
        f3 = Mess[i].find(',time:')
        f5 = Mess[i].find(',Agree')
        f6 = Mess[i].find(',Dis')
        if x == 3:
            if type == friOk and f5 != -1:
                Mess.remove(Mess[i])
            if type == friFall and f6 != -1:
                Mess.remove(Mess[i])
            if type == friReq and f2 != -1 and Mess[i][f1+5:f2] in s:
                Mess.remove(Mess[i])
# 好友列表
def FriPart(table,sock):
    st = ','
    for i in range(len(table)):
        st += table[i]
        if i != len(table)-1 :
            st += ','
    sock.send(st.encode())

def AddFriPart(usertable,NowID,sock):
    otherID = sock.recv(buffsize).decode()
    fritable = []
    SQLPart.readfriend(fritable,NowID)
    flaginfri = False
    for i in fritable:
        if i == otherID:
            flaginfri = True
    flagin = False 
    for x in usertable:
        if x['User_ID'] == otherID: flagin = True
    if flaginfri:
        sock.send(str(insheet).encode())
    elif not flagin:
        sock.send(str(notinsheet).encode())
    elif flagin:
        sock.send(str(ok).encode())
        Mess.append('To ' + otherID + ',From ' + NowID + ',FriendReq')

def DeleteFriPart(NowID,sock):
    DelID = sock.recv(buffsize).decode()
    fritable = []
    SQLPart.readfriend(fritable,NowID)
    flaginfri = False
    for i in fritable:
        if i == DelID:
            flaginfri = True
    if flaginfri == False:
        sock.send(str(notinsheet).encode())
    else:
        SQLPart.deletefri(NowID,DelID)
        SQLPart.deletefri(DelID,NowID)
        sock.send(str(ok).encode())

def AgreeFriPart(NowID,sock):
    AgrID = sock.recv(buffsize).decode()
    SQLPart.agreefri(NowID,AgrID)
    SQLPart.agreefri(AgrID,NowID)
    s = set()
    s.add(AgrID)
    deletemess(NowID,s,friReq)
    Mess.append('To '+AgrID+',From '+NowID+',AgreeFriReq')

def news(NowID,clientMess,clientAgree,clientDis,clientFrireq):
    if NowID != '':
        for i in range(len(Mess)):
            x = Mess[i].find(NowID)
            f1 = Mess[i].find('From ')
            f2 = Mess[i].find(',FriendReq')
            f3 = Mess[i].find(',time')
            f4 = Mess[i].find(',New')
            f5 = Mess[i].find(',Agree')
            f6 = Mess[i].find(',Dis')
            if x == 3:
                if f2 != -1 : clientFrireq.add(Mess[i][f1+5:f2])
                if f5 != -1 : clientAgree.add(Mess[i][f1+5:f5])
                if f6 != -1 : clientDis.add(Mess[i][f1+5:f6])
                if f4 != -1 : clientMess.add(Mess[i][f1+5:f3])

def tcplink(NowID,sock,addr):
    ma = False
    while True:
        try:
            clientMess = set()
            clientAgree = set()
            clientDis = set()
            clientFrireq = set()
            news(NowID,clientMess,clientAgree,clientDis,clientFrireq)
            print('Waiting For The Client''s Command.')
            sentence = sock.recv(buffsize).decode() # 获取客户发送的主命令
            try :
                sentence=(int)(sentence)
            except Exception as e: 
                if not sentence :
                    break  
                NowID = sentence
                ma = True
                continue
        except Exception as e:
            break

        #读取表格
        usertable = []
        SQLPart.readtable(usertable)
        # 登陆情况
        if sentence == (int)(regRequest):
            NowID = RegPart(sock)
            print('[System Message] '+ NowID +' Register and Login!')
        elif sentence == (int)(logRequest):
            NowID = LogPart(usertable,sock)
            print('[System Message] '+ NowID +' Login!')
        elif sentence == (int)(friRequest):
            ans = len(clientFrireq)+len(clientAgree)+len(clientMess)+len(clientDis)
            sock.send((str)(ans).encode())
            sock.recv(buffsize)
            fritable = []
            SQLPart.readfriend(fritable,NowID)
            FriPart(fritable,sock)
            print('[%s] Finish Sending Friend List!' % NowID)
        # 添加好友
        if sentence == (int)(addFri):
            AddFriPart(usertable,NowID,sock)
        if sentence == (int)(aggFri):
            AgreeFriPart(NowID,sock)
        if sentence == (int)(delFri):
            DeleteFriPart(NowID,sock)
        if sentence == (int)(disFri):
            DisID = sock.recv(buffsize).decode()
            s = set()
            s.add(DisID)
            deletemess(NowID,s,friReq)
            sleep(0.2)
            Mess.append('To '+DisID+',From '+NowID+',DisagreeFriReq')
        # 消息列表
        if sentence == newsNum:
            sock.send((str)(len(clientMess)).encode())
            sleep(0.2)
            for i in clientMess:
                sock.send(i.encode())
                sleep(0.1)
        if sentence == friOk:
            sock.send((str)(len(clientAgree)).encode())
            sleep(0.2)
            for i in clientAgree:
                sock.send(i.encode())
                sleep(0.1)
            deletemess(NowID,clientAgree,friOk)
        if sentence == friFall:
            sock.send((str)(len(clientDis)).encode())
            sleep(0.2)
            for i in clientDis:
                sock.send(i.encode())
                sleep(0.1)
            deletemess(NowID,clientDis,friFall)
        if sentence == friReq:
            sock.send((str)(len(clientFrireq)).encode())
            sleep(0.2)
            for i in clientFrireq:
                sock.send(i.encode())
                sleep(0.1)

        if sentence == chatFri:
            chatID = sock.recv(buffsize).decode()
            flag = False
            table = []
            SQLPart.readtable(table)
            for x in table:
                if x['User_ID'] == chatID and x['Online'] == True:
                    flag = True
            if not flag : 
                sock.send(str(friNotOnline).encode())
            else : 
                sock.send(str(ok).encode())
            sleep(0.2)

        if sentence == isMes:
            chatID = sock.recv(buffsize).decode()
            tmp = 0
            for i in range(len(Mess)):
                x = Mess[i].find(NowID)
                y = Mess[i].find(',From')
                z = Mess[i].find(',time')
                if x == 3 and y != -1 and z != -1:
                    if Mess[i][y+6:z] == chatID:
                        tmp += 1
            sock.send(str(tmp).encode())
            sleep(0.3)
            idx = []
            for i in range(len(Mess)):
                if tmp > 0 :
                    x1 = Mess[i].find(NowID)
                    y = Mess[i].find(',From')
                    z = Mess[i].find(',time')
                    if x1 == 3 and y != -1 and z != -1:
                        if Mess[i][y+6:z] == chatID:
                            tmp -= 1
                            sock.send(Mess[i].encode())
                            sleep(0.5)
                            fn = Mess[i].find(',New File,')
                            pn = Mess[i].find(',New Pict,')
                            if fn != -1:
                                SendFile.sendfile(tmp_path+Mess[i][fn+10:],sock)
                                os.remove(tmp_path+Mess[i][fn+10:])
                            if pn != -1:
                                SendFile.sendfile(tmp_path+Mess[i][pn+10:],sock)
                                os.remove(tmp_path+Mess[i][pn+10:])
                            sleep(0.3)
                            idx.append(i)
            for i in reversed(idx):
                Mess[i]=''
            print('[%s] Finish Refreshing Message List!' % NowID) 

        if sentence == chatBegin:
            Strmes = sock.recv(buffsize).decode()
            x = Strmes.find(',From')
            chatID = Strmes[3:x]
            flag = False
            table = []
            SQLPart.readtable(table)
            for x in table:
                if x['User_ID'] == chatID and x['Online'] == True:
                    flag = True
            if not flag : 
                sock.send(str(friNotOnline).encode())
            else : 
                sock.send(str(ok).encode())
                Mess.append(Strmes)

        # 主机接收文件、图片
        if sentence == fileSend:
            strfil = sock.recv(buffsize).decode()
            sleep(0.1)
            filename = SendFile.recvfile(tmp_path,sock)
            Mess.append(strfil+',New File,'+filename)
        if sentence == picSend:
            strfil = sock.recv(buffsize).decode()
            sleep(0.1)
            filename = SendFile.recvfile(tmp_path,sock)
            Mess.append(strfil+',New Pict,'+filename)

    g_conn_pool.remove(sock)
    if not ma:
        SQLPart.setOL(False,NowID) 
        if NowID != '' :
            print('-----------------------------')
            print('[Message] '+ NowID +' Logout!')
            print('-----------------------------')
    sock.close()

# __main__
serverSocket = socket(AF_INET, SOCK_STREAM) # 创建TCP欢迎套接字，使用IPv4协议
serverSocket.bind(('',serverPort)) # 将TCP欢迎套接字绑定到指定端口
serverSocket.listen(20) # 最大连接数
print("The Server Is Ready To Receive")

while True:
    connectionSocket, addr = serverSocket.accept() # 接收到客户连接请求后，建立新的TCP连接套接字
    g_conn_pool.append(connectionSocket)
    print('Accept A New Connection From %s:%s...' % addr)
    t = threading.Thread(target=tcplink,args=('',connectionSocket,addr))
    t.setDaemon(True)
    t.start()

serverSocket.close()

