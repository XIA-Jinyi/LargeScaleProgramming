from typing import Callable
from Model import User, Message, Response
import json
import socket
import Const
import time
import hashlib
import threading


class FriendListener:
    """好友监听器"""

    def __init__(self,
                 status_callback: Callable[[User], None],
                 new_callback: Callable[[User], None],
                 add_callback: Callable[[User], None],
                 delete_callback: Callable[[User], None],
                 init_callback: Callable[[list[User]], None]):
        """初始化好友监听器

        Args:
            status_callback (Callable[[User], None]): 好友状态改变时，回调此函数
            new_callback (Callable[[User], None]): 有新好友请求时，回调此函数
            add_callback (Callable[[User], None]): 新好友请求通过时，回调此函数
            delete_callback (Callable[[User], None]): 好友被删除时，回调此函数
            init_callback (Callable[[list[User]], None]): 初始化好友列表时，回调此函数
        """
        self.status_callback = status_callback
        self.new_callback = new_callback
        self.add_callback = add_callback
        self.delete_callback = delete_callback
        self.init_callback = init_callback
        self.port = 20000
        not_found_port = True
        while not_found_port:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('0.0.0.0', self.port))
                not_found_port = False
            except:
                self.port += 1
        self.__sock = sock

    def __handle_conn(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        hold_conn = True
        while hold_conn:
            try:
                msg_bytes = conn.recv(Const.buf_len)
                msg = json.loads(msg_bytes.decode('utf-8'))
            except:
                hold_conn = False
                break
            if msg['op'] == 'status':
                user = User()
                user.email = msg['content']['email']
                user.status = msg['content']['status']
                print('FriendListener: Call status_callback.')
                self.status_callback(user)
            elif msg['op'] == 'new':
                user = User()
                user.email = msg['content']['email']
                user.username = msg['content']['username']
                print('FriendListener: Call new_callback.')
                self.new_callback(user)
            elif msg['op'] == 'add':
                user = User()
                user.email = msg['content']['email']
                user.username = msg['content']['username']
                user.status = msg['content']['status']
                print('FriendListener: Call add_callback.')
                self.add_callback(user)
            elif msg['op'] == 'delete':
                user = User()
                user.email = msg['content']['email']
                print('FriendListener: Call delete_callback.')
                self.delete_callback(user)
            elif msg['op'] == 'init':
                users = []
                for friend in msg['content']['friends']:
                    user = User()
                    user.email = friend['email']
                    user.username = friend['username']
                    user.status = friend['status']
                    users.append(user)
                print('FriendListener: Call init_callback.')
                self.init_callback(users)
            else:
                hold_conn = False
        conn.close()

    def __listen(self) -> None:
        self.__sock.listen(8)
        while True:
            conn, addr = self.__sock.accept()
            handle_thread = threading.Thread(target=self.__handle_conn, args=(conn, addr))
            handle_thread.daemon = True
            handle_thread.start()

    def run(self) -> None:
        """启动好友监听器"""
        listen_thread = threading.Thread(target=self.__listen)
        listen_thread.daemon = True
        listen_thread.start()


class PeerListener:
    """伙伴监听器"""

    def __init__(self, recv_callback: Callable[[str, float, Message], None]):
        """初始化伙伴监听器

        Args:
            recv_callback (Callable[[str, float, Message], None]): 收到消息后，回调此函数，参数依次为邮件地址、时间戳、消息
        """
        self.callback = recv_callback
        self.port = 30000
        not_found_port = True
        while not_found_port:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('0.0.0.0', self.port))
                not_found_port = False
            except:
                self.port -= 1
        self.__sock = sock

    def __handle_conn(self, conn: socket.socket, addr: tuple[str, int]):
        hold_conn = True
        while hold_conn:
            try:
                msg_bytes = conn.recv(Const.buf_len)
                msg = json.loads(msg_bytes.decode('utf-8'))
            except:
                hold_conn = False
                break
            # message = Message()
            # message.attributes = msg[0]['attributes']
            # message.content = msg[0]['content']
            self.callback(msg[1], time.time(), msg[0])
        conn.close()

    def __listen(self):
        self.__sock.listen(8)
        while True:
            conn, addr = self.__sock.accept()
            handle_thread = threading.Thread(target=self.__handle_conn, args=(conn, addr))
            handle_thread.daemon = True
            handle_thread.start()

    def run(self) -> None:
        """启动伙伴监听器"""
        listen_thread = threading.Thread(target=self.__listen)
        listen_thread.daemon = True
        listen_thread.start()


class ServerConnection:
    """服务器连接"""

    def __init__(self):
        """初始化服务器连接"""
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__is_sock_closed = True
        self.last_response = Response()
        """上一次的消息响应"""
        self.username = ''
        """用户名"""
        self.email = ''

    def connect(self) -> Response:
        """连接到服务器

        Returns:
            Response: 响应
        """
        errno = self.__sock.connect_ex((Const.server_ip, Const.server_port))
        retval = Response()
        retval.source = Response.Source.Server
        if errno != 0:
            retval.status = Response.Status.BadConnection
            retval.content = {'errno': errno, 'message': 'Connecting socket failed.'}
            return retval
        self.__is_sock_closed = False
        retval.status = Response.Status.Positive
        return retval


    def __send(self, op: str = 'hello', **kwargs) -> Response:
        retval = Response()
        retval.source = Response.Source.Server
        retval.status = Response.Status.BadConnection
        if self.__is_sock_closed:
            retval.content = {'message': 'Socket closed.'}
            return retval
        msg = {'op': op, 'content': kwargs}
        try:
            self.__sock.send(json.dumps(msg).encode('utf-8'))
        except:
            retval.content = {'message': 'Sending failed.'}
            return retval
        try:
            echo = self.__sock.recv(Const.buf_len)
        except:
            retval.content = {'message': 'Receiving failed.'}
            return retval
        try:
            echo = json.loads(echo.decode('utf-8'))
            retval.status = Response.Status(echo['status'])
            retval.content = echo['content']
        except:
            retval.Status = Response.Status.OtherError
            retval.content = {'message': 'Parsing message failed.'}
        return retval


    def refresh(self) -> Response:
        """刷新连接

        Returns:
            Response: 响应
        """
        return self.__send()

    def update_vericode(self, email: str) -> Response:
        """更新验证码并发送邮件
        
        Args:
            email (str): 电子邮件地址
            
        Returns:
            Response: 响应
        """
        return self.__send('update_vericode', email=email)

    def register(self, email: str, username: str, password: str, vericode: str) -> Response:
        """注册

        Args:
            username (str): 用户名
            password (str): 密码
            vericode (str): 验证码

        Returns:
            Response: 响应
        """
        pwdhash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return self.__send('register', email=email, username=username, pwdhash=pwdhash, vericode=vericode)

    def password_login(self, email: str, password: str) -> Response:
        """密码登录

        Args:
            email (str): 邮件地址
            password (str): 密码原文

        Returns:
            Response: 响应
        """
        self.email = email
        response = self.__send('password_login', email=email, pwdhash=hashlib.sha256(password.encode('utf-8')).hexdigest())
        if response.status == Response.Status.Positive:
            self.username = response.content['name']
        return response

    def vericode_login(self, email: str, vericode: str) -> Response:
        """验证码登录

        Args:
            email (str): 邮箱地址
            vericode (str): 验证码

        Returns:
            Response: 响应
        """
        self.email = email
        response = self.__send('vericode_login', email=email, vericode=vericode)
        if response.status == Response.Status.Positive:
            self.username = response.content['name']
        return response

    def bind_friend_listener(self, friend_listener: FriendListener) -> Response:
        """绑定好友监听器

        Args:
            friend_listener (FriendListener): 好友监听器

        Returns:
            Response: 响应
        """
        return self.__send('bind_friend_listener', port=friend_listener.port)

    def bind_peer_listener(self, peer_listener: PeerListener) -> Response:
        """绑定伙伴监听器

        Args:
            peer_listener (PeerListener): 好友监听器

        Returns:
            Response: 响应
        """
        return self.__send('bind_peer_listener', port=peer_listener.port)

    def find_user(self, user_email: str) -> Response:
        """查找用户

        Args:
            user_email (str): 邮件地址

        Returns:
            Response: 响应
        """
        return self.__send('find_user', email=user_email)

    def add_friend(self, friend_email: str) -> Response:
        """添加好友

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        return self.__send('add_friend', email=friend_email)

    def confirm_friend(self, friend_email: str) -> Response:
        """确认添加好友

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        return self.__send('confirm_friend', email=friend_email)

    def delete_friend(self, friend_email: str) -> Response:
        """删除好友

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        return self.__send('delete_friend', email=friend_email)

    def start_chat(self, friend_email: str) -> Response:
        """发起对话

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        self.last_response = self.__send('start_chat', email=friend_email)
        self.last_response.content['my_email'] = self.email
        return self.last_response

    def close(self) -> Response:
        """关闭连接

        Returns:
            Response: 响应
        """
        return self.__send('close')


class PeerSender:
    """伙伴发送器"""

    def __init__(self, server_response: Response):
        """初始化伙伴发送器

        Args:
            server_response (Response): `ServerConnection.start_chat` 的返回值
        """
        self.dest_email: str = server_response.content['email']
        self.dest_ip: str = server_response.content['ip']
        self.dest_port: int = server_response.content['port']
        self.email = server_response.content['my_email']
        self.last_response = Response()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.dest_ip, self.dest_port))
        pass

    def send(self, message: Message) -> Response:
        """发送消息

        Args:
            message (Message): 消息对象

        Returns:
            Response: 响应
        """
        msg_str = json.dumps([message, self.email])
        self.__sock.send(msg_str.encode())

    def close(self) -> Response:
        """关闭连接

        Returns:
            Response: 响应
        """
        self.__sock.close()


if __name__ == '__main__':
    def status_call(user):
        print(f'Receive status {user.__dict__}')
    def add_call(user):
        print(f'Receive add {user.__dict__}')
    def new_call(user):
        print(f'Receive new {user.__dict__}')
    def del_call(user):
        print(f'Receive delete {user.__dict__}')
    def init_call(l):
        print(f'Init friend list {[u.__dict__ for u in l]}')
    def show_call(email, t, msg):
        print(f'Receive message from {email}: {msg}')
    
    hint = input('Hint:\n')
    my_email, friend_email = 'jinyi.xia@bupt.edu.cn', '20230628101050@bupt.edu.cn'
    if hint == '1':
        my_email, friend_email = friend_email, my_email
        time.sleep(0.5)

    sc = ServerConnection()
    r = sc.connect()
    if r.status != Response.Status.Positive:
        exit(0)
    
    r = sc.password_login(my_email, '123456')
    print(f'[{hint}]password_login: {r.status} {r.content}')
    time.sleep(1)
    print()

    friend_listener = FriendListener(status_call, new_call, add_call, del_call, init_call)
    friend_listener.run()
    r = sc.bind_friend_listener(friend_listener)
    print(f'[{hint}]bind_friend_listener: {r.status} {r.content}')
    time.sleep(1)
    print()

    peer_listener = PeerListener(show_call)
    peer_listener.run()
    r = sc.bind_peer_listener(peer_listener)
    print(f'[{hint}]bind_peer_listener: {r.status} {r.content}')
    time.sleep(1)
    print()

    # if hint == '1':
    #     r = sc.add_friend(friend_email)
    #     print(f'add_friend: {r.status} {r.content}')
    #     time.sleep(1)
    #     print()
    # else:
    #     r = sc.confirm_friend(friend_email)
    #     print(f'confirm_friend: {r.status} {r.content}')
    #     time.sleep(1)
    #     print()

    # r = sc.delete_friend(friend_email)
    # print(f'delete_friend: {r.status} {r.content}')
    # time.sleep(1)
    # print()

    r = sc.start_chat(friend_email)
    print(f'[{hint}]start_chat: {r.status} {r.content}')
    time.sleep(1)
    print()

    if r.status == Response.Status.Positive:
        sender = PeerSender(r)
        msg = Message()
        msg.content = f'msg{hint}'
        sender.send(f'msg{hint}')

    time.sleep(2)
    r = sc.close()
    print(f'[{hint}]close: {r.status} {r.content}')
