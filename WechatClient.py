from socket import *
from tkinter import *
import os
import struct
import threading
import tkinter.messagebox
import time
import datetime

#常量列表####################################################################
logRequest = 100 #登录
regRequest = 101 #注册
chatBegin = b'104'
ok = 666 #成功
#notConnected = 999 #没有连接到服务器
done = 'Finish' #完成
#登录失败
fallOfNo = 601 #失败原因：该用户没有注册
fallOfWP = 602 #失败原因：密码错误
#注册失败
fallOfI = 610 #失败原因：用户名非法
fallOfA = 611 #失败原因：用户名已占用
#好友界面按钮
friRequest = '102' #请求获得好友列表
friNotOnline = b'103' #好友不在线，无法聊天
delFri = b'801'
addFri = b'800'
chatFri = b'888'
newsNum = b'802' #新消息数目
friOk = b'803' #好友申请成功数目
friFall = b'804' #好友申请失败数目
friReq = b'805' #收到好友申请数目
isMes = b'850' #是否有新消息
aggFri = b'810'
disFri = b'811'
fileSend = b'1000'
picSend = b'1001'
yes = 851
no = 852
insheet = 901 # 失败原因：用户已经在好友列表中
notinsheet = 903 # 失败原因：该用户名未注册
notFri = 904 # 失败原因：对方不是你的好友
serverName = '127.0.0.1' # 指定服务器地址
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM) # 建立TCP套接字，使用IPv4协议
clientSocket.connect((serverName,serverPort)) # 向服务器发起连接

global clientSocket2
global clientSocket3
#变量列表#####################################################################
numm=0
desFlag = True
retFlag = True
firstTime1 = True
firstTime2 = True
sss = ""
thePath = ".\\"
per = ""
tier = ""
friList = []
my_photos = []
ind = 0
rec = ""
#函数部分#####################################################################
#登陆界面
def log():
        global sss
        window=Tk()
        window.title('Hello~QwQ')
        window.geometry('250x300')
        #放个图
        f_right = Frame(height = 200,width = 154)   #创建<图片分区>
        photo = PhotoImage(file = '.\\img\\titi.gif')
        label = Label(f_right,image = photo) #右侧分区中添加标签（绑定图片）
        label.image = photo
        f_right.place(x = 30,y = 0) #图片显示分区
        label.grid() #加载标签控件
        #标签 用户名密码
        Label(window,text='用户名:').place(x=10,y=160)
        Label(window,text='密码:').place(x=10,y=200)
        Label(window,text='用户名和密码都不可以是纯数字哦！').place(x=30,y=220)
        #用户名输入框
        var_usr_name=StringVar()
        entry_usr_name=Entry(window,textvariable=var_usr_name)
        entry_usr_name.place(x=60,y=160)
        #密码输入框
        var_usr_pwd=StringVar()
        entry_usr_pwd=Entry(window,textvariable=var_usr_pwd,show='*')
        entry_usr_pwd.place(x=60,y=200)
        
        #关闭
        def usrquit():
            window.destroy()
        #注册
        def Reg(): #用户名，密码，是否是登录
            global sss
            name=var_usr_name.get()
            password=var_usr_pwd.get() 
            if (name == ''):
                tkinter.messagebox.showinfo('提示','请输入用户名！')
                return
            elif (password == ''):
                tkinter.messagebox.showinfo('提示','请输入密码！')
                return
            Req = (str)(regRequest).encode() #登录
            clientSocket.send(Req)
            Req = name.encode() #name
            clientSocket.send(Req)
            time.sleep(0.1)
            Req = password.encode() #password
            clientSocket.send(Req)
            Res = clientSocket.recvfrom(1024)
            Res = (int)(Res[0].decode())
            if(Res == ok):
                global clientSocket2
                clientSocket2 = socket(AF_INET, SOCK_STREAM)
                clientSocket2.connect((serverName,serverPort))
                global clientSocket3
                clientSocket3 = socket(AF_INET, SOCK_STREAM)
                clientSocket3.connect((serverName,serverPort))
                sss = name
                # name = ','+name
                Req = name.encode() #jian li xian cheng
                clientSocket2.send(Req)
                clientSocket3.send(Req)
                tkinter.messagebox.showinfo('提示','注册成功！已自动登录~')
                window.destroy()
                fri()### 转入好友列表界面。
                return  
            elif(Res == fallOfI):
                tkinter.messagebox.showinfo('提示',"用户名非法，请输入长度4-20、包含字母，且只包含数字和字母的用户名！QAQ")
                return
            elif(Res == fallOfA):
                tkinter.messagebox.showinfo('提示',"用户名已经被占用啦，换一个吧~")
                return
        #登录
        def Log():
            global sss
            name=var_usr_name.get()
            password=var_usr_pwd.get()
            if (name == ''):
                tkinter.messagebox.showinfo('提示','请输入用户名！')
                return
            elif (password == ''):
                tkinter.messagebox.showinfo('提示','请输入密码！')
                return
            Req = (str)(logRequest).encode() #登录
            clientSocket.send(Req)
            Req = name.encode() #name
            clientSocket.send(Req)
            time.sleep(0.3)
            Req = password.encode() #password
            clientSocket.send(Req)
            Res = clientSocket.recvfrom(1024)
            Res = (int)(Res[0].decode())
            if(Res == ok):
                global clientSocket2
                clientSocket2 = socket(AF_INET, SOCK_STREAM)
                clientSocket2.connect((serverName,serverPort))
                global clientSocket3
                clientSocket3 = socket(AF_INET, SOCK_STREAM)
                clientSocket3.connect((serverName,serverPort))
                
                sss = name
                # name = ','+name
                Req = name.encode() #jian li xian cheng
                clientSocket2.send(Req)
                clientSocket3.send(Req)
                tkinter.messagebox.showinfo('提示', '登录成功~')
                window.destroy()
                fri()#Friends
                return
            elif(Res == fallOfWP):
                tkinter.messagebox.showinfo("提示", "用户名或密码错误。")
                return
        bt_login=Button(window,text='登录',command=Log)
        bt_login.place(x=40,y=250)
        bt_logup=Button(window,text='注册',command=Reg)
        bt_logup.place(x=110,y=250)
        bt_logquit=Button(window,text='退出',command=usrquit)
        bt_logquit.place(x=180,y=250)
        window.mainloop()

def fri():
        global sss
        global desFlag
        global friList
        global firstTime1
        global window
        window = Tk()
        window.title('Hello,'+sss+'!')
        window.geometry('360x450')
        friList = []
        desFlag = False
        #刷新好友列表
        def refresh():
                global desFlag
                global friList
                global clientSocket3
                while True:
                        #if desFlag:
                        #       time.sleep(2)
                        #       continue
                        friList.clear()
                        Req = friRequest.encode()
                        clientSocket3.send(Req)
                        Res = clientSocket3.recvfrom(1024)
                        Res = Res[0].decode()
                        Req = friRequest.encode()
                        clientSocket3.send(Req)
                        print(Res)
                        mytext.delete('1.0','end')
                        if Res!='0':
                                mytext.insert('insert','|-------------------------------|\n')
                                mytext.insert('insert','|*您有新消息！                  |\n')
                                mytext.insert('insert','|*请点击消息列表查看！          |\n')
                                mytext.insert('insert','|-------------------------------|\n')
                        Res = clientSocket3.recvfrom(1024)
                        Res = Res[0].decode()
                        Res = Res[1:] #################################################################################
                        t = 0
                        for i in range(0,len(Res)):
                                if Res[i]==',':
                                        if t != 0:
                                                t = t+1
                                        friList.append(Res[t:i])
                                        t = i
                        if t != 0:
                                t = t+1
                        friList.append(Res[t:len(Res)])
                        mytext.insert('insert','输入好友名字即可和ta聊天！~\n\n')
                        mytext.insert('insert','~~~~~~好友列表~~~~~~~~~~~~\n')
                        mytext.insert('insert','~~~~~~~~~~~~~~~~~~~~~~~~~\n')
                        for i in range(0,len(friList)):
                                x = friList[i]
                                mytext.insert('insert','      '+x+'\n')
                        time.sleep(1)
        def cha():
                global sss
                global per
                global retFlag
                retFlag = False
                tk = Toplevel()
                tk.geometry('500x500')
                tk.title('和'+per+'聊天~')
                def msgsend(): #向per发送一次消息
                    #发送接收消息
                    global per
                    sentence = txt_msgsend.get('0.0',END)
                    Req = chatBegin #发送开始聊天请求
                    clientSocket.send(Req)
                    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    mes = 'To '+per+',From '+sss+',time:'+timeNow+',New Mess,'+sentence
                    time.sleep(0.3)
                    Req = mes.encode()
                    clientSocket.send(Req)
                    Res = clientSocket.recvfrom(1024)
                    Res = (int)(Res[0].decode())
                    if Res != ok:
                            tkinter.messagebox.showinfo('提示','好友已经不在线，或已不再您好友列表。消息发送失败。')
                    else:
                            msg = ' 我'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
                            txt_msglist.insert(END,msg,'green') #添加时间
                            txt_msglist.insert(END,' '+txt_msgsend.get('0.0',END)) #获取发送消息，添加文本到消息列表
                            txt_msgsend.delete('0.0',END) #清空发送消息
                def cancel():
                    txt_msgsend.delete('0.0',END) #取消发送消息，即清空发送消息
                #接收消息###########
                def recv():
                        global thePath
                        global per
                        global retFlag
                        global clientSocket2
                        print('qqqqqqqqqqqq')
                        while True:
                                time.sleep(1)
                                if retFlag:
                                        return
                                Req = isMes #询问是否有新消息,新消息数目
                                clientSocket2.send(Req)
                                time.sleep(0.2)
                                Req = per.encode()
                                clientSocket2.send(Req)
                                Ress = clientSocket2.recvfrom(1024)
                                Ress = (int)(Ress[0].decode())
                                print(Ress)
                                while Ress:
                                        Ress = Ress-1
                                        Res = clientSocket2.recvfrom(1024)
                                        print(Res)
                                        Res = (str)(Res[0].decode())
                                        if Res.count(',New Mess,') != 0:
                                                x = Res.find(',From')
                                                Res = Res[x+5:]
                                                x = Res.find(',time:')
                                                tmp = Res[x+6:Res.find(',New Mess,')]
                                                msg = Res[0:x]+' '+tmp+'\n'  
                                                txt_msglist.insert(END,msg,'green') #添加时间
                                                Res = Res[Res.find(',New Mess,')+10:]
                                                txt_msglist.insert(END,' '+Res+'\n')
                                        elif Res.count(',New File,') != 0:
                                                x = Res.find(',From')
                                                Res = Res[x+5:]
                                                x = Res.find(',time:')
                                                tmp = Res[x+6:Res.find(',New File,')]
                                                msg = Res[0:x]+' '+tmp+'\n'  
                                                txt_msglist.insert(END,msg,'green') #添加时间
                                                Res = Res[Res.find(',New File,')+10:]
                                                txt_msglist.insert(END," 向你发送了一个文件"+Res+",存至默认路径:"+thePath+'\n')
                                                # 接收文件
                                                fileinfo_size = struct.calcsize('128sl')
                                                buf = clientSocket2.recv(fileinfo_size)
                                                if buf:
                                                        filename, filesize = struct.unpack('128sl', buf)
                                                        fn = filename.strip(b'\00')
                                                        fn = fn.decode()
                                                        print ('file new name is {0}, filesize if {1}'.format(str(fn),filesize))
                                                        recvd_size = 0  # 定义已接收文件的大小
                                                        fp = open(thePath+fn, 'wb')
                                                        print ('start receiving...')
                                                        while not recvd_size == filesize:
                                                                if filesize - recvd_size > 1024:
                                                                        data = clientSocket2.recv(1024)
                                                                        recvd_size += len(data)
                                                                else:
                                                                        data = clientSocket2.recv(filesize - recvd_size)
                                                                        recvd_size = filesize
                                                                fp.write(data)
                                                        fp.close()
                                                        print ('end receive...')
                                        elif Res.count(',New Pict,') != 0:
                                                x = Res.find(',From')
                                                Res = Res[x+5:]
                                                x = Res.find(',time:')
                                                tmp = Res[x+6:Res.find(',New Pict,')]
                                                msg = Res[0:x]+' '+tmp+'\n'  
                                                txt_msglist.insert(END,msg,'green') #添加时间
                                                Res = Res[Res.find(',New Pict,')+10:]
                                                # 接收图片
                                                fileinfo_size = struct.calcsize('128sl')
                                                buf = clientSocket2.recv(fileinfo_size)
                                                if buf:
                                                        filename, filesize = struct.unpack('128sl', buf)
                                                        fn = filename.strip(b'\00')
                                                        fn = fn.decode()
                                                        print ('file new name is {0}, filesize if {1}'.format(str(fn),filesize))
                                                        recvd_size = 0  # 定义已接收文件的大小
                                                        fp = open(thePath+fn, 'wb')
                                                        print ('start receiving...')
                                                        while not recvd_size == filesize:
                                                                if filesize - recvd_size > 1024:
                                                                        data = clientSocket2.recv(1024)
                                                                        recvd_size += len(data)
                                                                else:
                                                                        data = clientSocket2.recv(filesize - recvd_size)
                                                                        recvd_size = filesize
                                                                fp.write(data)
                                                        fp.close()
                                                        print ('end receive...')
                                                # 显示图片
                                                global my_photos
                                                global ind
                                                my_photos.append(PhotoImage(file=thePath+fn))
                                                txt_msglist.image_create(END, image=my_photos[ind])
                                                txt_msglist.insert(END,'\n')
                                                ind = ind + 1
                global rec
                global firstTime2
                rec = threading.Timer(1, recv)
                rec.start()
                firstTime2 = False
                def EndChat():
                        global retFlag
                        retFlag = True
                        tk.destroy()
                        # fri()
                        return
                def Sendpic():
                        def msgs():
                                filepath = url.get()
                                x = filepath.find('.')
                                if filepath[x+1:]!='png' and filepath[x+1:]!='gif':
                                        tkinter.messagebox.showinfo("提示","发送失败，目前只支持发送png和gif类型的图片哦！")
                                        return
                                if os.path.isfile(filepath):
                                        clientSocket.send(picSend)
                                        print(filepath)
                                        mess = 'To '+per+',From '+sss+',time:'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        clientSocket.send(mess.encode())
                                        fileinfo_size = struct.calcsize('128sl')
                                        fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
                                        print('11111111111111111111111111')
                                        time.sleep(0.2)
                                        clientSocket.send(fhead)
                                        fp = open(filepath, 'rb')
                                        while 1:
                                                data = fp.read(1024)
                                                if not data:
                                                        print ('{0} file send over...'.format(os.path.basename(filepath)))
                                                        break
                                                clientSocket.send(data)
                                        tkinter.messagebox.showinfo("提示","发送成功！")
                                        tt.destroy()
                                        msg = ' 我'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
                                        txt_msglist.insert(END,msg,'green') #添加时间
                                        global my_photos
                                        global ind
                                        my_photos.append(PhotoImage(file=filepath))
                                        txt_msglist.image_create(END, image=my_photos[ind])
                                        txt_msglist.insert(END,'\n')
                                        ind = ind + 1
                                else :
                                        tkinter.messagebox.showinfo("提示","不是合法路径！再检查一下吧！")
                        tt = Toplevel()
                        tt.geometry('430x80')
                        url=StringVar()
                        ent=Entry(tt,textvariable=url,width=50)
                        ent.place(x=10,y=35)
                        Label(tt,text='图片路径:').place(x=10,y=5)
                        bu = Button(tt,text = 'Send',command = msgs)
                        bu.place(x=370,y=30)
                        tt.mainloop()
                        print("will return")
                        return
                def Sendfile():
                        def msgs():
                                global per
                                global sss
                                filepath = url.get()
                                if os.path.isfile(filepath):
                                        clientSocket.send(fileSend)
                                        print(filepath)
                                        mess = 'To '+per+',From '+sss+',time:'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        clientSocket.send(mess.encode())
                                        fileinfo_size = struct.calcsize('128sl')
                                        fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
                                        print('11111111111111111111111111')
                                        time.sleep(0.2)
                                        clientSocket.send(fhead)
                                        fp = open(filepath, 'rb')
                                        while 1:
                                                data = fp.read(1024)
                                                if not data:
                                                        print ('{0} file send over...'.format(os.path.basename(filepath)))
                                                        break
                                                clientSocket.send(data)
                                        tkinter.messagebox.showinfo("提示","发送成功！")
                                        tt.destroy()
                                        msg = ' 我'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
                                        txt_msglist.insert(END,msg,'green') #添加时间
                                        txt_msglist.insert(END,' 向对方发送了一个文件\n')
                                else :
                                        tkinter.messagebox.showinfo("提示","不是合法路径！再检查一下吧！")
                        tt = Toplevel()
                        tt.geometry('430x80')
                        url=StringVar()
                        ent=Entry(tt,textvariable=url,width=50)
                        ent.place(x=10,y=35)
                        Label(tt,text='文件路径:').place(x=10,y=5)
                        bu = Button(tt,text = 'Send',command = msgs)
                        bu.place(x=370,y=30)
                        tt.mainloop()
                def Recfile():
                        def msgs():
                                global thePath
                                filepath = url.get()
                                if os.path.isdir(filepath):
                                        thePath = filepath
                                        tkinter.messagebox.showinfo("提示","修改成功！")
                                        tt.destroy()
                                        return
                                else :
                                        tkinter.messagebox.showinfo("提示","不是合法路径！再检查一下吧！")
                        tt = Toplevel()
                        tt.geometry('430x80')
                        url=StringVar()
                        ent=Entry(tt,textvariable=url,width=50)
                        ent.place(x=10,y=35)
                        Label(tt,text='文件路径:').place(x=10,y=5)
                        bu = Button(tt,text = 'Send',command = msgs)
                        bu.place(x=370,y=30)
                        tt.mainloop()
                #绑定up键
                def msgsendEvent(event):
                        if event.keysym == 'Up':
                                msgsend()
                
                #创建分区
                f_msglist = Frame(tk,height = 300,width = 500) #创建<消息列表分区 >  
                f_msgsend = Frame(tk,height = 170,width = 500) #创建<发送消息分区 >
                f_floor = Frame(tk,height = 30,width = 500)   #创建<按钮分区>
                 
                #创建控件
                txt_msglist = Text(f_msglist) #消息列表分区中创建文本控件
                txt_msglist.tag_config('green',foreground = 'blue') #消息列表分区中创建标签
                txt_msgsend = Text(f_msgsend) #发送消息分区中创建文本控件
                txt_msgsend.bind('<KeyPress-Up>',msgsendEvent) #发送消息分区中，绑定‘UP’键与消息发送。
                #txt_right = Text(f_right) #图片显示分区创建文本控件'''
                button_send = Button(f_floor,text = 'Send',command = msgsend) #按钮分区中创建按钮并绑定发送消息函数
                button_cancel = Button(f_floor,text = 'Cancel',command = cancel) #分区中创建取消按钮并绑定取消函数
                button_back = Button(f_floor,text = 'Back',command = EndChat)
                button_pic = Button(f_floor,text = 'Send Pic!',command = Sendpic)
                button_file = Button(f_floor,text = 'Send File!',command = Sendfile)
                button_recfile = Button(f_floor,text = 'Set Path!',command = Recfile)#设置文件保存路径
                #分区布局
                f_msglist.place(x=0,y=0) #消息列表分区
                f_msgsend.place(x=0,y=301)  #发送消息分区
                f_floor.place(x=0,y=471)    #按钮分区
                txt_msglist.grid()  #消息列表文本控件加载
                txt_msgsend.grid()  #消息发送文本控件加载
                button_send.grid(row = 0,column = 0,sticky = W)   #发送按钮控件加载
                button_cancel.grid(row = 0,column = 1,sticky = W) #取消按钮控件加载
                button_back.grid(row = 0,column = 2,sticky = W)
                button_pic.grid(row = 0,column = 3,sticky = W)
                button_file.grid(row = 0,column = 4,sticky = W)
                button_recfile.grid(row = 0,column = 5,sticky = W)
                tk.mainloop()
        #聊天按钮
        def Connect(perr=''): #尝试与per建立连接
                if perr=='':
                        perr = _name.get()
                if perr=='':
                        print("No per")
                        return
                print("getttt")
                global friList
                if not (perr in friList):
                        tkinter.messagebox.showinfo("提示","对方还不是你的好友！~")
                        return
                global per
                per = perr
                Req = chatFri
                clientSocket.send(Req)
                time.sleep(0.1)
                Req = per.encode()
                clientSocket.send(Req)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                if(Res != ok):
                        print(Res)
                        tkinter.messagebox.showinfo("提示","你的好友不在线哦！等ta在线了再来找ta吧~")
                        return
                elif(Res == ok):
                        cha()
        #添加好友
        def addfri():
                per=_name.get()
                if per=='':
                        return
                Req = addFri
                clientSocket.send(Req)
                Req = per.encode()
                clientSocket.send(Req)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                if Res == insheet:#已经是好友
                        tkinter.messagebox.showinfo("提示","添加好友失败，你们已经是好友啦！")
                elif Res == notinsheet:#没有这个人
                        tkinter.messagebox.showinfo("提示","添加好友失败，该用户没有注册！")
                elif Res == ok:#添加成功
                        tkinter.messagebox.showinfo("提示","已发送好友请求，正在等待对方通过申请~！")
        #删除按钮
        def delete():
                per = _name.get()
                if per=='':
                        return
                Req = delFri
                clientSocket.send(Req)
                Req = per.encode()
                clientSocket.send(Req)
                print(per)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                print(Res)
                if Res == notinsheet:#没有这个人
                        tkinter.messagebox.showinfo("提示","删除好友失败，该用户不在您的好友列表里哦！")
                elif Res == ok:#删除成功
                        tkinter.messagebox.showinfo("提示","删除成功！")

        def news():
                winn = Toplevel()
                winn.title('Hey '+sss+',your message!')
                winn.geometry('480x450')
                global numm
                _opp = StringVar()
                opet = Entry(winn,textvariable= _opp )
                opet.place(x=10,y=10)
                           
                scroll = tkinter.Scrollbar()
                mytex=Text(winn,width=300,height=500,font='FangSong')
                mytex.pack(padx=10,pady=80)
                scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
                mytex.pack(side=tkinter.LEFT,fill=tkinter.Y)
                scroll.config(command=mytex.yview) # 将滚动条与文本框关联
                mytex.config(yscrollcommand=scroll.set) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
                mytex.window_create(INSERT)
                #tip#######################
                mytex.insert('insert','|--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--|\n')
                mytex.insert('insert','|tips: 在框框里输入ta的名字即可回复消息！^_^|\n')
                mytex.insert('insert','|*在框框里输入\'+\'+ta的编号即可同意好友申请！|\n')
                mytex.insert('insert','|*在框框里输入\'-\'+ta的编号即可拒绝好友申请！|\n')
                mytex.insert('insert','|--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--|\n')
                #请求##########
                #新消息
                Req = newsNum
                clientSocket.send(Req)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                # Res = 0
                mytex.insert('insert','|-------------------------------------------|\n')
                if Res==0:
                        mytex.insert('insert','|*0*没有收到聊天！--------------------------|\n')
                        mytex.insert('insert','|-------------------------------------------|\n')
                else :
                        while Res:
                                Res = Res-1
                                Ress = clientSocket.recvfrom(1024)
                                Ress = (str)(Ress[0].decode())
                                mytex.insert('insert','|收到'+Ress+'的新消息！~\n')
                        mytex.insert('insert','|-------------------------------------------|\n')
                #好友申请成功
                Req = friOk
                clientSocket.send(Req)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                # Res = 0
                if Res==0:
                        pass
                else :
                        while Res:
                                Res = Res-1
                                Ress = clientSocket.recvfrom(1024)
                                Ress = (str)(Ress[0].decode())
                                mytex.insert('insert','|OvO!:'+Ress+'通过了你的好友申请！~\n')
                        mytex.insert('insert','|-------------------------------------------|\n')
                #好友申请失败
                Req = friFall
                clientSocket.send(Req)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                if Res==0:
                        pass
                else :
                        while Res:
                                Res = Res-1
                                Ress = clientSocket.recvfrom(1024)
                                Ress = (str)(Ress[0].decode())
                                mytex.insert('insert','|TAT…:'+Ress+'拒绝和你成为好友。\n')
                        mytex.insert('insert','|-------------------------------------------|\n')
                #收到好友申请
                Req = friReq
                clientSocket.send(Req)
                Res = clientSocket.recvfrom(1024)
                Res = (int)(Res[0].decode())
                lis = []
                if Res==0:
                        mytex.insert('insert','|*0*没有收到好友申请！----------------------|\n')
                        mytex.insert('insert','|-------------------------------------------|\n')
                else :
                        numm = 0
                        while Res:
                                numm = numm+1
                                Res = Res-1
                                Ress = clientSocket.recvfrom(1024)
                                Ress = (str)(Ress[0].decode())
                                lis.append(Ress)
                                mytex.insert('insert','|收到'+Ress+'的好友申请！~编号:')
                                mytex.insert('insert',numm)
                                mytex.insert('insert','\n')
                        mytex.insert('insert','|-------------------------------------------|\n')
                #按钮###########
                def proc():
                        global numm
                        global firList
                        op = _opp.get()
                        if op == '':
                                pass
                        elif op[0] != '+' and op[0] != '-':
                                if friList.count(op) != 0:
                                        Connect(op)
                                else:
                                        tkinter.messagebox.showinfo("提示",op +"不是您的好友哦！")
                        else :
                                p = op[0]
                                op = op+'+'
                                tmp = 1
                                for i in range(1,len(op)):
                                      if op[i] == '+' or op[i] == '-' :
                                                name = op[tmp:i]
                                                name = int(name,base=10)
                                                global numm
                                                if name > numm:
                                                        tkinter.messagebox.showinfo("提示",str(name) +"不是合法的编号哦！")
                                                        continue
                                                if lis[name-1]=='000':
                                                        continue
                                                if p == '+':
                                                        clientSocket.send(aggFri)
                                                else :
                                                        clientSocket.send(disFri)
                                                Req = lis[name-1].encode()
                                                clientSocket.send(Req)
                                                lis[name-1] = '000'
                                                tmp = i+1
                                tkinter.messagebox.showinfo("提示","Over，ser!")
                bt666=Button(winn,text = "@v@///over!~~~",command = proc )
                bt666.place(x=160,y=5)
                
                winn.mainloop()  
                #插入文本#######
                #mytex.insert('insert','|-------------------------------------------|\n')
                
        def logOut():
                Req = ''
                Req = Req.encode()
                clientSocket.send(Req)
                clientSocket.close()
                clientSocket2.close()
                clientSocket3.close()
                tkinter.messagebox.showinfo("提示","注销成功，拜拜~!")
                window.destroy()
                return
        #####################
        #多线程
        global tier
        global firstTime1
        if firstTime1:
                tier = threading.Timer(1, refresh)
                tier.start()
        firstTime1 = False
        #加载按钮
        bt0=Button(window,text="消息列表",command = news)
        bt0.place(x=155,y=5)
        #文本框
        _name = StringVar()
        ent=Entry(window,textvariable = _name)
        #删除按钮
        bt3=Button(window,text="删除框框里的ta",command = delete )
        #聊天按钮
        bt2=Button(window,text='和框框里的ta聊天',command = Connect )
        #添加好友
        bt=Button(window,text="添加框框里的ta",command = addfri)
        # 注销登录
        bt00=Button(window,text="~~注销~~",command = logOut)
        bt00.place(x=250,y=5)
        #框#############
        scroll = tkinter.Scrollbar()
        mytext=Text(window,width=300,height=500,font='FangSong')
        mytext.pack(padx=10,pady=80)
        bt.place(x=215,y=45)
        bt2.place(x=10,y=45)
        bt3.place(x=119,y=45)
        ent.place(x=10,y=10)
        # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        # 将文本框填充进wuya窗口的左侧
        mytext.pack(side=tkinter.LEFT,fill=tkinter.Y)
        # 将滚动条与文本框关联
        scroll.config(command=mytext.yview)
        # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        mytext.config(yscrollcommand=scroll.set)
        mytext.window_create(INSERT)
        window.mainloop()   

#主程序开始#########################################################################
log()
clientSocket.close()
clientSocket2.close()
