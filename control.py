from ClientService.Communication import ServerConnection,FriendListener
from ClientService.Model import Response,User
from threading import Lock

sc = ServerConnection()
friend_ls=[]
friend_ls_lock = Lock()
friend_new_ls=[]
#new_friend_cnt=0
def get_verify():
    #和前端沟通如何将验证码传入
    pass
def get_service_type():
    #和前端沟通怎样去确认服务类型
    pass
def login(email,pwd):#如果成功返回1，错误返回0，后面跟返回码
    global sc
    if pwd=='':
        #验证码登录
        response=sc.update_vericode(email)
        if response!=Response.Status.Positive:
            #连接错误,返回0和错误码
            return 0,response.status
        else:
            #验证码发送正确
            ver_code=get_verify()
            response=sc.vericode_login(email,ver_code)
            if response!=Response.Status.Positive:
                #连接错误或者验证码错误
                #if response==Response.Status.NegativeClose:
                sc.close()
                return 0,response.status
            else:
                #登陆成功
                return 1,0
    else:
        #密码登录
        response=sc.password_login(email,pwd)
        if response!=Response.Status.Positive:
            #连接错误或者密码错误
            sc.close()
            return 0,response.status
        else:
            return 1,0

def register(email,username,pwd):#如果成功返回1，错误返回0，后面跟返回码
    global sc
    sc.update_vericode(email)   #发验证码邮件
    if sc.last_response.status!=Response.Status.Positive:
        ver_code=get_verify()   #发送成功，让用户输入验证码
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
def init_friend_list(friedn_ls):
    global friend_ls
    friend_ls_lock.acquire()
    friend_ls_lock.release()
    return



if __name__ == '__main__':
    response=sc.connect()
    if response.status!=Response.Status.Positive:
        exit(0)
    friend=FriendListener(update_friend_status(),
                          new_friend_request(),
                          add_new_friend(),
                          delete_friend(),init_friend_list())
    friend.run()
    sc.bind_friend_listener(friend)
    while True:
        while sc.last_response==Response.Status.Positive:
            #接收前端信息，选择服务类型
            service=get_service_type()
        sc.refresh()
    '''
    print(func())
    sc = ServerConnection()
    response = sc.connect()
    if response.status != Response.Status.Positive:
        exit(0)
    sc.update_vericode('123@abc.com')
    sc.vericode_login('123@abc.com', '123123')'''