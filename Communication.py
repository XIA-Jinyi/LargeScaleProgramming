from typing import Callable
from Model import User, Message, Response
import json
import socket
import Const
import time


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
        pass

    def run(self) -> None:
        """启动好友监听器"""
        pass


class ServerConnection:
    """服务器连接"""

    def __init__(self):
        """初始化服务器连接"""
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__is_sock_closed = True
        self.last_response = Response()
        """上一次的消息响应"""

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
            retval.content = Response.Status(echo['content'])
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
        pass

    def register(email: str, username: str, password: str, vericode: str) -> Response:
        """注册

        Args:
            username (str): 用户名
            password (str): 密码
            vericode (str): 验证码

        Returns:
            Response: 响应
        """
        pass

    def password_login(self, email: str, password: str) -> Response:
        """密码登录

        Args:
            email (str): 邮件地址
            password (str): 密码原文

        Returns:
            Response: 响应
        """
        pass

    def vericode_login(self, email: str, vericode: str) -> Response:
        """验证码登录

        Args:
            email (str): 邮箱地址
            vericode (str): 验证码

        Returns:
            Response: 响应
        """
        pass

    def bind_friend_listener(self, friend_listener: FriendListener) -> Response:
        """绑定好友监听器

        Args:
            friend_listener (FriendListener): 好友监听器

        Returns:
            Response: 响应
        """
        pass

    def find_user(self, user_email: str) -> Response:
        """查找用户

        Args:
            user_email (str): 邮件地址

        Returns:
            Response: 响应
        """
        pass

    def add_friend(self, friend_email: str) -> Response:
        """添加好友

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        pass

    def confirm_friend(self, friend_email: str) -> Response:
        """确认添加好友

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        pass

    def delete_friend(self, friend_email: str) -> Response:
        """删除好友

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        pass

    def start_chat(self, friend_email: str) -> Response:
        """发起对话

        Args:
            friend_email (str): 邮箱地址

        Returns:
            Response: 响应
        """
        pass

    def close(self) -> Response:
        """关闭连接

        Returns:
            Response: 响应
        """
        return self.__send('close')


class PeerListener:
    """伙伴监听器"""

    def __init__(self, recv_callback: Callable[[str, float, Message], None]):
        """初始化伙伴监听器

        Args:
            recv_callback (Callable[[str, float, Message], None]): 收到消息后，回调此函数，参数依次为邮件地址、时间戳、消息
        """
        self.callback = recv_callback
        pass

    def run(self) -> None:
        """启动伙伴监听器"""
        pass


class PeerSender:
    """伙伴发送器"""

    def __init__(self, server_response: Response):
        """初始化伙伴发送器

        Args:
            server_response (Response): `ServerConnection.start_chat` 的返回值
        """
        self.dest_email: str = None
        self.dest_ip: str = None
        self.dest_port: int = None
        self.last_response = Response()
        pass

    def send(self, message: Message) -> Response:
        """发送消息

        Args:
            message (Message): 消息对象

        Returns:
            Response: 响应
        """
        pass

    def close(self) -> Response:
        """关闭连接

        Returns:
            Response: 响应
        """
        pass


if __name__ == '__main__':
    hint = input('Hint: ')
    sc = ServerConnection()
    sc.connect()
    while True:
        print(sc.refresh().status)
        time.sleep(2)