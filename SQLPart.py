import xlrd
from xlrd import xldate_as_tuple
import datetime
import xlwt
from xlutils import copy
sure = 1 #确认
cancel = 2 #取消
back = 3 #后退
logRequest = 100 #登录
regRequest = 101 #注册
friRequest = 102 #请求获得好友列表
friNotOnline = 103 #好友不在线，无法聊天
chatBegin = 104
ok = 666 #成功
#notConnected = 999 #没有连接到服务器
done = "@" #完成
#登录失败
fallOfNo = 601 #失败原因：该用户没有注册
fallOfWP = 602 #失败原因：密码错误
#注册失败
fallOfI = 610 #失败原因：用户名非法
fallOfA = 611 #失败原因：用户名已占用
tables = []

# 读入表格
def readtable(table_x):
   data1 = xlrd.open_workbook(r'.\\database\\UserInform.xls')
   table = data1.sheets()[0]
   #将excel表格内容导入到tables列表中
   def import_excel(excel):
      for rown in range(1,excel.nrows):
         array = {'User_ID':'','Password':'','Online':bool}
         array['User_ID'] = str(table.cell_value(rown,0))
         array['Password'] = str(table.cell_value(rown,1))
         array['Online'] = table.cell_value(rown,2)
         table_x.append(array)
   import_excel(table)

# 找到好友列表
def readfriend(table_x,id): 
   data1 = xlrd.open_workbook('.\\database\\'+id+'.xls')
   table = data1.sheets()[0]
   for rown in range(1,table.nrows):
      array = str(table.cell_value(rown,0))
      table_x.append(array)


# 查找是否可以登录
def find(table_x,uid,upa):
   for us in table_x:
      if us['User_ID'] == uid and us['Password'] == upa:
         return ok
   return fallOfWP

# 新建好友列表
def creat_table(newid):
   book = xlwt.Workbook(encoding='utf-8')
   sheet = book.add_sheet('friends')
   idpath = '.\\database\\'+newid + '.xls'
   sheet.write(0,0,'好友昵称')
   book.save(idpath)

# 注册
def register(newid,newpa):
   newid = (str)(newid)
   if newid.isdigit() or newpa.isdigit():
      return  fallOfI 
   datap = xlrd.open_workbook(r'.\\database\\UserInform.xls')
   tmp = datap.sheets()[0]
   for rown in range(tmp.nrows):
      if newid == tmp.cell_value(rown,0):
         return fallOfA
   datan = copy.copy(datap)
   table = datan.get_sheet(0)
   row = tmp.nrows
   table.write(row,0,newid)
   table.write(row,1,newpa)
   table.write(row,2,True)
   datan.save('.\\database\\UserInform.xls')
   creat_table(newid)
   return ok

# 设置在线或离线
def setOL(f,id):
   datatmp = xlrd.open_workbook(r'.\\database\\UserInform.xls')
   tmp = datatmp.sheets()[0]
   datach = copy.copy(datatmp)
   ta = datach.get_sheet(0)
   for rown in range(1,tmp.nrows):
      if tmp.cell_value(rown,0) == id:
         ta.write(rown,2,f)
         break
   datach.save('.\\database\\UserInform.xls')

# 删除好友
def deletefri(ida,idb):
   datatmp = xlrd.open_workbook('.\\database\\'+ida+'.xls')
   tmp = datatmp.sheets()[0]
   datach = copy.copy(datatmp)
   fri = datach.get_sheet(0)
   r = 0
   print(tmp.nrows)
   for rown in range(1,tmp.nrows):
      if tmp.cell_value(rown,0) == idb:
         r = rown
         break
   if r==0: return
   for rown in range(r,tmp.nrows-1):
      fri.write(rown,0,tmp.cell_value(rown+1,0))
   fri.write(tmp.nrows-1,0,None)
   datach.save('.\\database\\'+ida+'.xls')

def agreefri(ida,idb):
   datatmp = xlrd.open_workbook('.\\database\\'+ida+'.xls')
   tmp = datatmp.sheets()[0]
   datach = copy.copy(datatmp)
   fri = datach.get_sheet(0)
   fri.write(tmp.nrows,0,idb)
   datach.save('.\\database\\'+ida+'.xls')  
