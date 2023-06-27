from ClientService import Const, Model
from ServerService import Database, Survival
import socket
import threading
import json
import random
import time
import sqlite3


db_conn = sqlite3.connect('server.db')
localhost = '0.0.0.0'
port = Const.server_port
vericode_dict = {'email@demo.domain': ('123456', time.time())}
online_dict = {'email@demo.domain': (False, time.time())}
friend_listener_dict = {'email@demo.domain': ('ip', 22222)}
peer_listener_dict = {'email@demo.domain': ('ip', 22222)}
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


def handle_hello(conn, addr) -> None:
    respond(conn)


def handle_close(conn, addr) -> None:
    respond(conn, close=True)


def handle_update_vericode(conn, addr, email) -> None:
    vericode = ''.join(random.choice('1234567890QWERTYUIOPASDFGHJKLZXCVBNM0987654321') for _ in range(6))
    with vericode_dict_lock:
        vericode_dict[email] = (vericode, time.time())
    print(f'Vericode Updated: {email} ({vericode})')
    respond(conn)


def handle_register(conn, addr, email: str, username: str, password: str, vericode: str) -> bool:
    with vericode_dict_lock:
        if vericode_dict.get(email, None) is None:
            respond(conn, False, close=True, message='Vericode not requested')
            return False
        if vericode_dict[email][0] != vericode:
            respond(conn, False, close=True, message='Wrong vericode')
            return False
        if vericode_dict[email][1] + Survival.Vericode > time.time():
            respond(conn, False, close=True, message='Vericode expired')
            return False
    if Database.find_user(db_conn, email) != None:
        respond(conn, False, close=True, message='Email already registered')
        return False
    Database.register(db_conn, email, username, password)
    respond(conn)
    return True


def handle_password_login(conn, addr, email: str, password: str) -> bool:
    pwdhash = Database.get_pwdhash(db_conn, email)
    if pwdhash == None:
        respond(conn, False, close=True, message='Email not registered')
        return False
    if pwdhash != password:
        respond(conn, False, close=True, message='Wrong password')
        return False
    username = Database.find_user(db_conn, email)
    with online_dict_lock:
        if online_dict.get(email, (False, None)):
            respond(conn, False, close=True, message='Already online')
            return False
        online_dict[email] = (True, time.time())
    respond(conn, name=username)
    return True


def handle_vericode_login(conn, addr, email: str, vericode: str) -> bool:
    username = Database.find_user(db_conn, email)
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
        if vericode_dict[email][1] + Survival.Vericode > time.time():
            respond(conn, False, close=True, message='Vericode expired')
            return False
    with online_dict_lock:
        if online_dict.get(email, (False, None)):
            respond(conn, False, close=True, message='Already online')
            return False
        online_dict[email] = (True, time.time())
    respond(conn, name=username)
    return True


def handle_bind_friend_listener(conn, addr, email, friend_listener_port: int):
    with friend_listener_dict_lock:
        friend_listener_dict[email] = (addr[0], friend_listener_port)
    respond(conn)


def handle_bind_peer_listener(conn, addr, email, peer_listener_port: int):
    with peer_listener_dict_lock:
        peer_listener_dict[email] = (addr[0], peer_listener_port)
    respond(conn)


def handle_find_user(conn, addr, email: str) -> bool:
    username = Database.find_user(db_conn, email)
    if username == None:
        respond(conn, False, message='Email not registered')
        return False
    respond(conn, name=username)
    return True


def handle_add_friend(conn, addr, user_email, friend_email: str):
    if Database.judge_friend(db_conn, user_email, friend_email):
        respond(conn, False, message='Already friends')
        return False
    Database.raise_friend_request(db_conn, user_email, friend_email)
    respond(conn)
    return True


def handle_confirm_friend(conn, addr, user_email, friend_email: str):
    if Database.judge_friend(db_conn, user_email, friend_email):
        respond(conn, False, message='Already friends')
        return False
    Database.add_friend(db_conn, user_email, friend_email)
    respond(conn)
    return True


def handle_delete_friend(conn, addr, user_email, friend_email: str):
    Database.del_friend(db_conn, user_email, friend_email)
    respond(conn)


def handle_start_chat(conn, addr, user_email, friend_email: str):
    with online_dict_lock:
        if not online_dict.get(friend_email, (False, None))[0]:
            respond(conn, False, message='Friend offline')
            return False
    with peer_listener_dict_lock:
        if peer_listener_dict.get(friend_email, None) is None:
            respond(conn, False, message='Friend not listening')
            return False
        peer_listener_addr = peer_listener_dict[friend_email]
    respond(conn, ip=peer_listener_addr[0], port=peer_listener_addr[1])


def server_thread(conn: socket.socket, addr):
    hold_conn = True
    email = None
    print(f'{addr[0]}:{addr[1]} connected')
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
    print(f'{addr[0]}:{addr[1]} closed')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((localhost, port))
    sock.listen(16)
    print(f'Server running at {localhost}:{port}')
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=server_thread, args=(conn, addr))
        thread.daemon = True
        thread.start()
