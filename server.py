from ClientService import Const, Model
from ServerService import Database, Survival
import socket
import threading
import json
import random
import time
import atexit
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base64


db_path = os.path.abspath('server.db')
localhost = '0.0.0.0'
port = Const.server_port
vericode_dict = {'email@demo.domain': ('123456', time.time())}
online_dict = {'email@demo.domain': (False, time.time())}
friend_listener_dict = {'email@demo.domain': (Const.server_ip, Const.server_port)}
peer_listener_dict = {'email@demo.domain': (Const.server_ip, Const.server_port)}
username_dict = {'email@demo.domain': 'demoname'}
vericode_dict_lock = threading.Lock()
online_dict_lock = threading.Lock()
friend_listener_dict_lock = threading.Lock()
peer_listener_dict_lock = threading.Lock()


def respond(conn, positive: bool = True, close: bool = False, **kwargs):
    if positive == True and close == False:
        status = Model.Response.Status.Positive.value
    elif positive == True and close == True:
        status = Model.Response.Status.PositiveClose.value
    elif positive == False and close == False:
        status = Model.Response.Status.Negative.value
    elif positive == False and close == True:
        status = Model.Response.Status.NegativeClose.value
    conn.send(json.dumps({'status': status, 'content': kwargs}).encode())


def operate(conn, op: str, **kwargs):
    conn.send(json.dumps({'op': op, 'content': kwargs}).encode())


def send_email(email: str, vericode: str) -> bool:
    with vericode_dict_lock:
        vericode_dict[email] = (vericode, time.time())
        print(f'\033[34m{email}: {vericode}\033[0m')
    mail_html = f"""<p class=MsoNormal style='layout-grid-mode:char'><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>您的验证码为：</span><span lang=EN-US style='font-size:14.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-theme-font:
minor-bidi'><o:p></o:p></span></p>
<p class=MsoNormal align=center style='margin-top:7.8pt;margin-right:0cm;
margin-bottom:7.8pt;margin-left:0cm;mso-para-margin-top:.5gd;mso-para-margin-right:
0cm;mso-para-margin-bottom:.5gd;mso-para-margin-left:0cm;text-align:center;
layout-grid-mode:char'><b><span lang=EN-US style='font-size:22.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-font-family:Arial;
letter-spacing:3.0pt'>{vericode}<o:p></o:p></span></b></p>
<p class=MsoNormal style='layout-grid-mode:char'><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>此验证码包含数字与大写英文字母，输入时请注意字母大小写是否正确。验证码</span><span lang=EN-US
style='font-size:14.0pt;font-family:"Times New Roman",serif;mso-fareast-font-family:
宋体;mso-bidi-theme-font:minor-bidi'>10</span><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>分钟内有效。</span><span lang=EN-US style='font-size:14.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-theme-font:
minor-bidi'><o:p></o:p></span></p>"""
    message = MIMEText(mail_html, 'html', 'utf-8')
    message['From'] = 'Server <jinyi.xia@foxmail.com>'
    message['To'] = f'<{email}>'
    message['Subject'] = Header("验证码", 'utf-8')
    retval = True
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com')
        server.login('jinyi.xia@foxmail.com', 'owkqtmqtphhpdhhi')
        server.sendmail('jinyi.xia@foxmail.com', [email], message.as_string())
        server.quit()
    except:
        retval = True #False
    return retval


def handle_hello(conn, addr) -> None:
    respond(conn)


def handle_close(conn, addr) -> None:
    respond(conn, close=True)


def handle_update_vericode(conn, addr, email) -> None:
    vericode = ''.join(random.choice('23456789QWERTYUPASDFGHJKZXCVBNM98765432') for _ in range(6))
    if send_email(email, vericode):
        with vericode_dict_lock:
            vericode_dict[email] = (vericode, time.time())
        respond(conn)
        print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Vericode Updated: {email} <\033[36m{vericode}\033[0m>')
    else:
        respond(conn, False)
    respond(conn)


def handle_register(conn, addr, email: str, username: str, password: str, vericode: str) -> bool:
    with vericode_dict_lock:
        if vericode_dict.get(email, None) is None:
            respond(conn, False, close=True, message='Vericode not requested')
            return False
        if vericode_dict[email][0] != vericode:
            respond(conn, False, close=True, message='Wrong vericode')
            return False
        current_time = time.time()
        if vericode_dict[email][1] + Survival.Vericode < current_time:
            respond(conn, False, close=True, message='Vericode expired')
            return False
    if Database.find_user(db_path, email) != None:
        respond(conn, False, close=True, message='Email already registered')
        return False
    Database.register(db_path, email, username, password)
    respond(conn)
    return True


def handle_password_login(conn, addr, email: str, password: str) -> bool:
    pwdhash = Database.get_pwdhash(db_path, email)
    if pwdhash == None:
        respond(conn, False, close=True, message='Email not registered')
        return False
    if pwdhash != password:
        respond(conn, False, close=True, message='Wrong password')
        return False
    username = Database.find_user(db_path, email)
    with online_dict_lock:
        if online_dict.get(email, (False, None))[0]:
            respond(conn, False, close=True, message='Already online')
            return False
        online_dict[email] = (True, time.time())
    respond(conn, name=username)
    return True


def handle_vericode_login(conn, addr, email: str, vericode: str) -> bool:
    username = Database.find_user(db_path, email)
    if username == None:
        respond(conn, False, close=True, message='Email not registered')
        return False
    with vericode_dict_lock:
        if vericode_dict.get(email, None) is None:
            respond(conn, False, close=True, message='Vericode not requested')
            return False
        if vericode_dict[email][0] != vericode:
            respond(conn, False, close=True, message='Wrong vericode')
            return False
        if vericode_dict[email][1] + Survival.Vericode < time.time():
            respond(conn, False, close=True, message='Vericode expired')
            return False
    with online_dict_lock:
        if online_dict.get(email, (False, None))[0]:
            respond(conn, False, close=True, message='Already online')
            return False
        online_dict[email] = (True, time.time())
    respond(conn, name=username)
    return True


def handle_bind_friend_listener(conn, addr, email, friend_listener_port: int):
    with friend_listener_dict_lock:
        friend_listener_dict[email] = (addr[0], friend_listener_port)
    # Broadcast online status to friends
    friend_list = Database.get_friend_list(db_path, email)
    friends: list[Model.User] = []
    with online_dict_lock:
        for friend_tuple in friend_list:
            friend = Model.User()
            friend.email = friend_tuple[0]
            friend.username = friend_tuple[1]
            if online_dict.get(friend_tuple[0], (False, None))[0]:
                friend.status = Model.User.Status.Online
            else:
                friend.status = Model.User.Status.Offline
            friends.append(friend)
    for friend in friends:
        if friend.status == Model.User.Status.Online:
            with friend_listener_dict_lock:
                friend_addr = friend_listener_dict.get(friend.email, None)
            if friend_addr is None:
                continue
            friend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            friend_conn.connect(friend_addr)
            operate(friend_conn, 'status', email=email, status=Model.User.Status.Online.value)
            friend_conn.close()
    # Feedback
    new_friend_requests = Database.get_friend_request(db_path, email)
    self_listener_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self_listener_conn.connect((addr[0], friend_listener_port))
    operate(self_listener_conn,
            'init',
            friends=[{'email': friend.email,
                      'username': friend.username,
                      'status': friend.status.value}
                      for friend in friends])
    self_listener_conn.close()
    for new_tuple in new_friend_requests:
        self_listener_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self_listener_conn.connect((addr[0], friend_listener_port))
        operate(self_listener_conn,
                'new',
                email=new_tuple[0],
                username=new_tuple[1])
        self_listener_conn.close()
    respond(conn)


def handle_bind_peer_listener(conn, addr, email, peer_listener_port: int):
    with peer_listener_dict_lock:
        peer_listener_dict[email] = (addr[0], peer_listener_port)
    respond(conn)


def handle_find_user(conn, addr, email: str) -> bool:
    username = Database.find_user(db_path, email)
    if username == None:
        respond(conn, False, message='Email not registered')
        return False
    respond(conn, name=username)
    return True


def handle_add_friend(conn, addr, user_email, friend_email: str):
    if Database.judge_friend(db_path, user_email, friend_email):
        respond(conn, False, message='Already friends')
        return False
    # Check if friend online
    online = False
    with online_dict_lock:
        online = online_dict.get(friend_email, (False, None))[0]
    if online:
        # Send friend request
        with friend_listener_dict_lock:
            friend_addr = friend_listener_dict.get(friend_email, None)
        friend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        friend_conn.connect(friend_addr)
        operate(friend_conn,
                'new',
                email=user_email,
                username=Database.find_user(db_path, user_email))
        friend_conn.close()
    else:
        Database.raise_friend_request(db_path, user_email, friend_email)
    respond(conn)
    return True


def handle_confirm_friend(conn, addr, user_email, friend_email: str):
    if Database.judge_friend(db_path, user_email, friend_email):
        respond(conn, False, message='Already friends')
        return False
    # Check if friend online
    online = False
    with online_dict_lock:
        online = online_dict.get(friend_email, (False, None))[0]
    if online:
        # Send friend request
        with friend_listener_dict_lock:
            friend_addr = friend_listener_dict.get(friend_email, None)
        friend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        friend_conn.connect(friend_addr)
        operate(friend_conn,
                'add',
                email=user_email,
                username=Database.find_user(db_path, user_email),
                status=Model.User.Status.Online.value)
        friend_conn.close()
    self_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with friend_listener_dict_lock:
        self_listenner_addr = friend_listener_dict[user_email]
    self_conn.connect(self_listenner_addr)
    operate(self_conn,
            'add',
            email=friend_email,
            username=Database.find_user(db_path, friend_email),
            status=Model.User.Status.Online.value if online else Model.User.Status.Offline.value)
    self_conn.close()
    Database.add_friend(db_path, user_email, friend_email)
    respond(conn)
    return True


def handle_delete_friend(conn, addr, user_email, friend_email: str):
    # Check if friend online
    online = False
    with online_dict_lock:
        online = online_dict.get(friend_email, (False, None))[0]
    if online:
        if not Database.judge_friend(db_path, user_email, friend_email):
            respond(conn, True, message='Not friends')
            return False
        # Send delete request
        with friend_listener_dict_lock:
            friend_addr = friend_listener_dict.get(friend_email, None)
        friend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        friend_conn.connect(friend_addr)
        operate(friend_conn,
                'delete',
                email=user_email)
        friend_conn.close()
    self_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with friend_listener_dict_lock:
        self_listenner_addr = friend_listener_dict[user_email]
    self_conn.connect(self_listenner_addr)
    operate(self_conn,
            'delete',
            email=user_email)
    self_conn.close()
    Database.del_friend(db_path, user_email, friend_email)
    respond(conn)


def handle_start_chat(conn, addr, user_email, friend_email: str):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Start chat from <{user_email}> to <{friend_email}>')
    with online_dict_lock:
        if not online_dict.get(friend_email, (False, None))[0]:
            respond(conn, False, message='Friend offline')
            return False
    with peer_listener_dict_lock:
        if peer_listener_dict.get(friend_email, None) is None:
            respond(conn, False, message='Friend not listening')
            return False
        peer_listener_addr = peer_listener_dict[friend_email]
    respond(conn, ip=peer_listener_addr[0], port=peer_listener_addr[1], email=friend_email)


def server_thread(conn: socket.socket, addr):
    hold_conn = True
    email = None
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Connected')
    while hold_conn:
        try:
            msg_bytes = conn.recv(Const.buf_len)
            msg = json.loads(msg_bytes.decode('utf-8'))
        except:
            hold_conn = False
            break
        if msg['op'] == 'hello':
            handle_hello(conn, addr)
        elif msg['op'] == 'close':
            handle_close(conn, addr)
            hold_conn = False
        elif msg['op'] == 'register':
            if handle_register(conn, addr, msg['content']['email'], msg['content']['username'], msg['content']['pwdhash'], msg['content']['vericode']):
                email = msg['content']['email']
            hold_conn = False
        elif msg['op'] == 'update_vericode':
            handle_update_vericode(conn, addr, msg['content']['email'])
        elif msg['op'] == 'password_login':
            if handle_password_login(conn, addr, msg['content']['email'], msg['content']['pwdhash']):
                email = msg['content']['email']
            else:
                hold_conn = False
        elif msg['op'] == 'vericode_login':
            if handle_vericode_login(conn, addr, msg['content']['email'], msg['content']['vericode']):
                email = msg['content']['email']
            else:
                hold_conn = False
        elif msg['op'] == 'bind_friend_listener':
            if email is None:
                respond(conn, False, close=True, message='Not logged in')
                hold_conn = False
            handle_bind_friend_listener(conn, addr, email, msg['content']['port'])
        elif msg['op'] == 'bind_peer_listener':
            handle_bind_peer_listener(conn, addr, email, msg['content']['port'])
        elif msg['op'] == 'find_user':
            handle_find_user(conn, addr, msg['content']['email'])
        elif msg['op'] == 'add_friend':
            handle_add_friend(conn, addr, email, msg['content']['email'])
        elif msg['op'] == 'confirm_friend':
            handle_confirm_friend(conn, addr, email, msg['content']['email'])
        elif msg['op'] == 'delete_friend':
            handle_delete_friend(conn, addr, email, msg['content']['email'])
        elif msg['op'] == 'start_chat':
            handle_start_chat(conn, addr, email, msg['content']['email'])
        else:
            respond(conn, False, message='Unknown operation')   
    conn.close()
    if email is not None:
        with online_dict_lock:
            online_dict[email] = (False, time.time())
        with friend_listener_dict_lock:
            friend_listener_dict[email] = None
        with peer_listener_dict_lock:
            peer_listener_dict[email] = None
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m closed')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((localhost, port))
    sock.listen(16)
    atexit.register(sock.close)
    print(f'Server running at {localhost}:{port}')
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=server_thread, args=(conn, addr))
        thread.daemon = True
        thread.start()
