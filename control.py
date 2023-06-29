from Communication import *
from Model import *
from threading import Lock
import sqlite3
import base64
import time

message_db_con = sqlite3.connect('message.db')
sc = ServerConnection()
friend_ls = []
friend_ls_lock = Lock()
friend_new_ls = []
client_account = ''
ver_code = ''
P_sender = None
message = Message()
front_entity = None
friend = None
P_listener = None


def init():
    global sc
    global friend
    global P_listener
    sc.connect()
    friend = FriendListener(callbak_update_friend_status,
                            callbak_new_friend_request,
                            callbak_add_new_friend,
                            callbak_delete_friend, callbak_init_friend_list)

    friend.run()
    print("friend_runed")


def init_after_login(real_one):
    global friend
    global P_listener
    global sc
    update_front_entity(real_one)
    sc.bind_friend_listener(friend)
    print('friend_bind')
    P_listener = PeerListener(recv_message)
    P_listener.run()
    sc.bind_peer_listener(P_listener)


# new_friend_cnt=0
def update_front_entity(real_one):
    global front_entity
    front_entity = real_one
    return


def update_front_friend_ls():  # 提醒前端更新friend_list
    global front_entity
    front_entity.front_update_friend_ls()
    return


def update_front_friend_new_ls():  # 提醒前端更新好友申请列表
    global front_entity
    front_entity.front_update_friend_new_ls()
    return


def update_communication(email, message_str):
    global front_entity
    if email == front_entity.chatObject:
        front_entity.send_message(email, message_str)
    return


def build_message(message_str):  # 前后端信息格式转换
    global message
    message.attributes = {}
    message.content = message_str.encode("utf8")
    return


def get_verify(ver):
    # 和前端沟通如何将验证码传入
    global ver_code
    ver_code = ver
    return


def send_verify_code(email):
    global sc
    global client_account
    # 反复发验证码
    # sc = ServerConnection()
    # sc.connect()
    client_account = email
    sc.update_vericode(client_account)
    # 点输入验证码
    return


def login(email, pwd):  # 如果成功返回1，错误返回0，后面跟返回码
    global sc
    global client_account
    global ver_code
    global friend_ls
    global friend_new_ls
    global P_listener
    global friend

    client_account = email
    # 清空list
    friend_ls = []
    friend_new_ls = []
    sc = ServerConnection()
    sc.connect()
    if pwd == '':
        # 验证码登录
        # 验证码发送正确
        # ver_code=get_verify()
        response_lo = sc.vericode_login(email, ver_code)
        if response_lo.status != Response.Status.Positive:
            # 连接错误或者验证码错误
            # if response==Response.Status.NegativeClose:
            sc.close()
            sc = ServerConnection()
            sc.connect()
            return 0, response_lo.status
        else:
            # 登陆成功
            return 1, 0
    else:
        # 密码登录
        response_lo = sc.password_login(email, pwd)
        if response_lo.status != Response.Status.Positive:
            # 连接错误或者密码错误
            sc.close()
            sc = ServerConnection()
            sc.connect()
            return 0, response_lo.status
        else:
            return 1, 0


def register(email, username, pwd):  # 如果成功返回1，错误返回0，后面跟返回码
    global sc
    global ver_code
    # if sc.last_response == Response.Status.NegativeClose or sc.last_response == Response.Status.PositiveClose:
    sc = ServerConnection()
    sc.connect()
    # 发验证码邮件
    response = sc.register(email, username, pwd, ver_code)
    # print(sc.last_response.status)
    if response.status == Response.Status.Positive:
        # 验证成功，注册成功
        sc.close()
        sc = ServerConnection()
        sc.connect()
        sc.password_login(email, pwd)
        return 1, 0
    else:
        # 连接错误或验证失败
        sc.close()
        sc = ServerConnection()
        sc.connect()
        return 0, sc.last_response.status


def callbak_update_friend_status(user):
    global friend_ls
    friend_ls_lock.acquire()
    for i in range(len(friend_ls)):
        if user.email == friend_ls[i].email:
            friend_ls[i].status = user.status
            # friend_ls[i].username=user.username
            break
    friend_ls_lock.release()
    return


def callbak_new_friend_request(user):
    # 别人来的新好友请求，要和前端商量怎么提示
    print('new_friend_request')
    print(user.__dict__)
    global friend_new_ls
    friend_new_ls.append(user)
    update_front_friend_new_ls()
    return


def callbak_confirm_new_friend(user):
    # 确认新好友请求
    global friend_ls
    for i in range(len(friend_new_ls)):
        if friend_new_ls[i].email == user.email:
            del friend_new_ls[i]
            break
    friend_ls_lock.acquire()
    friend_ls.append(user)
    friend_ls_lock.release()
    update_front_friend_ls()
    update_front_friend_new_ls()
    return


def callbak_add_new_friend(user):
    # 我请求加别人好友，别人通过了
    global friend_ls
    friend_ls_lock.acquire()
    friend_ls.append(user)
    friend_ls_lock.release()
    update_front_friend_ls()
    return


def callbak_delete_friend(user):
    global friend_ls
    friend_ls_lock.acquire()
    for i in range(len(friend_ls)):
        if user.email == friend_ls[i].email:
            del friend_ls[i]
            break
    friend_ls_lock.release()
    update_front_friend_ls()
    return


def callbak_init_friend_list(acquired_friend_ls):
    global friend_ls
    print(acquired_friend_ls)
    friend_ls_lock.acquire()
    friend_ls = acquired_friend_ls
    friend_ls_lock.release()
    update_front_friend_ls()
    return


def recv_message(email, time_stamp, message_recv):
    global message_db_con
    global client_account
    while not message_db_con:
        message_db_con = sqlite3.connect('message.db')
    cursor = message_db_con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message'")
    result = cursor.fetchone()
    # 以base64编码存储数据
    base64_string = base64.b64encode(message_recv.content.decode("utf8"))
    if not result:
        # 没有表就建表
        cursor.execute('''CREATE TABLE message_T
                (sender CHAR(50)    NOT NULL,
                recver CHAR(50)     NOT NULL,
                timestamp FLOAT     NOT NULL,
                message CHAR(500)    NOT NULL);''')
    cursor.execute("INSERT INTO message_T (sender, recver, timestamp, message) VALUES (?, ?, ?, ?)",
                   (email, client_account, time_stamp, base64_string))
    message_db_con.commit()
    update_communication(email, message_recv.content.decode("utf8"))
    return


def send_message(target_email):
    global message
    global message_db_con
    global client_account
    global P_sender
    global sc
    while not message_db_con:
        message_db_con = sqlite3.connect('message.db')
    cursor = message_db_con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message'")
    result = cursor.fetchone()
    # 以base64编码存储数据
    base64_string = base64.b64encode(message.content.decode("utf8"))
    if not result:
        # 没有表就建表
        cursor.execute('''CREATE TABLE message_T
                (sender CHAR(50)    NOT NULL,
                recver CHAR(50)     NOT NULL,
                timestamp FLOAT     NOT NULL,
                message CHAR(500)    NOT NULL);''')
    # if not P_sender:
    P_sender = PeerSender(sc.start_chat(target_email))
    response_in = P_sender.send(message)
    if response_in.status == Response.Status.Positive:
        # base64_string = base64.b64encode(message.content).decode("utf8")
        cursor.execute("INSERT INTO message_T (sender, recver, timestamp, message) VALUES (?, ?, ?, ?)",
                       (client_account, target_email, time.time(), base64_string))
        message_db_con.commit()
    P_sender.close()
    return


def get_message(from_email):
    # 返回消息的base64编码，以$间隔
    global client_account
    global message_db_con
    while not message_db_con:
        message_db_con = sqlite3.connect('message.db')
    cursor = message_db_con.cursor()
    cursor.execute(
        f"SELECT sender,message FROM message_T WHERE (sender=\'{from_email}\' AND recver=\'{client_email}\')"
        f" OR (recver=\'{client_email}\' AND sender=\'{from_email}\') ORDER BY timestamp ascend")
    result = cursor.fetchall()

    """
    [('1_sender', '1_message'), ('2_sender', '2_message'),...]
    """
    # <分割1_sender,1_message,$分割1，2
    result_str = '$'.join('<'.join(group) for group in result)
    return result_str


def request_add_friend(target_email):  # 如果成功就返回1，不然就返回0和错误码(未知错误），返回-1表示用户已存在
    global sc
    sc.find_user(target_email)
    if sc.last_response.status != Response.Status.Positive:
    # 用户已存在
        return 2
    sc.add_friend(target_email)
    print(sc.last_response.__dict__)
    if sc.last_response.status != Response.Status.Positive:
        return 0
    else:
        return 1


def confirm_add_friend(target_email):  # 如果成功就返回1，不然就返回0和错误码
    global sc
    global friend_new_ls
    sc.confirm_friend(target_email)
    if sc.last_response.status != Response.Status.Positive:
        return 0
    else:
        for i in range(len(friend_new_ls)):
            if friend_new_ls[i].email == target_email:
                del friend_new_ls[i]
                break
        update_front_friend_new_ls()
        # update_front_friend_ls()
        return 1


def delete_friend(target_email):
    global sc
    sc.delete_friend(target_email)
    if sc.last_response.status != Response.Status.Positive:
        return 0
    else:
        return 1


if __name__ == '__main__':
    response = sc.connect()
    if response.status != Response.Status.Positive:
        exit(0)
    friend = FriendListener(callbak_update_friend_status,
                            callbak_new_friend_request,
                            callbak_add_new_friend,
                            callbak_delete_friend, callbak_init_friend_list)
    friend.run()
    sc.bind_friend_listener(friend)
    P_listener = PeerListener(recv_message)
    P_listener.run()
    sc.bind_peer_listener(P_listener)
