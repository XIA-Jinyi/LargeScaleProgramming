from ClientService.Communication import ServerConnection,FriendListener,PeerListener,PeerSender
from ClientService.Model import Response,User
from threading import Lock
import sqlite3
import base64
import time
message_db_con = sqlite3.connect('message.db')
sc = ServerConnection()
friend_ls=[]
friend_ls_lock = Lock()
friend_new_ls=[]
client_account=''
ver_code=''
P_sender=None
#new_friend_cnt=0
def get_verify():
    #和前端沟通如何将验证码传入
    global ver_code
    ver_code=''
    pass
def get_service_type():
    #和前端沟通怎样去确认服务类型
    pass
def send_verify_code():
    global sc
    #反复发验证码
    sc.update_vericode()
    #点输入验证码
    return
def login(email,pwd):#如果成功返回1，错误返回0，后面跟返回码
    global sc
    global client_account
    global ver_code
    if pwd=='':
        #验证码登录
        if response!=Response.Status.Positive:
            #连接错误,返回0和错误码
            return 0,response.status
        else:
            #验证码发送正确
            #ver_code=get_verify()
            response=sc.vericode_login(email,ver_code)
            if response!=Response.Status.Positive:
                #连接错误或者验证码错误
                #if response==Response.Status.NegativeClose:
                sc.close()
                return 0,response.status
            else:
                #登陆成功
                client_account=email
                return 1,0
    else:
        #密码登录
        response=sc.password_login(email,pwd)
        if response!=Response.Status.Positive:
            #连接错误或者密码错误
            sc.close()
            return 0,response.status
        else:
            client_account=email
            return 1,0

def register(email,username,pwd):#如果成功返回1，错误返回0，后面跟返回码
    global sc
    global ver_code
    #sc.update_vericode(email)
    #send_verify_code()
    #发验证码邮件
    if sc.last_response.status!=Response.Status.Positive:
        #ver_code=get_verify()   #发送成功，让用户输入验证码
        sc.register(email,username,pwd,ver_code)
        if sc.last_response.status!=Response.Status.Positive:
            #验证成功，注册成功
            return 1,0
        else:
            # 连接错误或验证失败
            sc.close()
            return 0, sc.last_response.status
    else:
        #连接错误
        sc.close()
        return 0,sc.last_response.status
def update_friend_status(user):
    global friend_ls
    friend_ls_lock.acquire()
    for i in range(len(friend_ls)):
        if user.email==friend_ls[i].email:
            friend_ls[i].status=user.status
            #friend_ls[i].username=user.username
            break
    friend_ls_lock.release()
    return

def new_friend_request(user):
    #新好友请求，要和前端商量怎么提示
    global friend_new_ls
    friend_new_ls.append(user)
    return
def add_new_friend(user):
    #确认新好友请求
    global friend_ls
    friend_ls_lock.acquire()
    friend_ls.append(user)
    friend_ls_lock.release()
    return
def delete_friend(user):
    global friend_ls
    friend_ls_lock.acquire()
    for i in range(len(friend_ls)):
        if user.email==friend_ls[i].email:
            del friend_ls[i]
            break
    friend_ls_lock.release()
    return
def init_friend_list(acquired_friend_ls):
    global friend_ls
    friend_ls_lock.acquire()
    friend_ls=acquired_friend_ls
    friend_ls_lock.release()
    return

def recv_message(email,time_stamp,message):
    global message_db_con
    global client_account
    while not message_db_con:
        message_db_con = sqlite3.connect('message.db')
    cursor = message_db_con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message'")
    result = cursor.fetchone()
    #以base64编码存储数据
    base64_string=base64.b64encode(message.content).decode("utf8")
    if not result:
        #没有表就建表
        cursor.execute('''CREATE TABLE message
                (sender CHAR(50)    NOT NULL,
                recver CHAR(50)     NOT NULL,
                timestamp FLOAT     NOT NULL,
                message CHAR(500)    NOT NULL);''')
    cursor.execute("INSERT INTO message (sender, recver, timestamp, message) VALUES (?, ?, ?, ?)",
                   (email, client_account, time_stamp, base64_string))
    message_db_con.commit()
    return
def send_message(target_email,message):
    global message_db_con
    global client_account
    global P_sender
    global sc
    while not message_db_con:
        message_db_con = sqlite3.connect('message.db')
    cursor = message_db_con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message'")
    result = cursor.fetchone()
    #以base64编码存储数据
    base64_string=base64.b64encode(message.content).decode("utf8")
    if not result:
        #没有表就建表
        conn.execute('''CREATE TABLE message
                (sender CHAR(50)    NOT NULL,
                recver CHAR(50)     NOT NULL,
                timestamp FLOAT     NOT NULL,
                message CHAR(500)    NOT NULL);''')
    if not P_sender:
        P_sender=PeerSender(sc.start_chat(target_email))
    P_sender.send(message)
    if sc.last_response==Response.Status.Positive:
        #base64_string = base64.b64encode(message.content).decode("utf8")
        cursor.execute("INSERT INTO message (sender, recver, timestamp, message) VALUES (?, ?, ?, ?)",
                       (client_email, target_email, time.time(), base64_string))
        message_db_con.commit()
    return
def add_friend(target_email):#如果成功就返回1，不然就返回0和错误码
    global sc
    sc.add_friend(target_email)
    if sc.last_response!=Response.Status.Positive:
        return 0,sc.last_response
    else :return 1,0
def delete_friend(target_email):
    global sc
    sc.delete_friend(target_email)
    if sc.last_response!=Response.Status.Positive:
        return 0,sc.last_response
    else :return 1,0

if __name__ == '__main__':
    response=sc.connect()
    if response.status!=Response.Status.Positive:
        exit(0)
    friend=FriendListener(update_friend_status,
                          new_friend_request,
                          add_new_friend,
                          delete_friend,init_friend_list)
    friend.run()
    sc.bind_friend_listener(friend)
    P_listener = PeerListener(recv_message)
    P_listener.run()
    while True:
        while sc.last_response==Response.Status.Positive:
            #接收前端信息，选择服务类型
            service=get_service_type()
        if sc.last_response==Response.Status.Timeout:
            sc.refresh()
        else:
            sc.connect()
    '''
    print(func())
    sc = ServerConnection()
    response = sc.connect()
    if response.status != Response.Status.Positive:
        exit(0)
    sc.update_vericode('123@abc.com')
    sc.vericode_login('123@abc.com', '123123')'''