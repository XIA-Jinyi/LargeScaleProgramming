from enum import Enum
from typing import Callable


class Response:
    """消息响应"""

    class Status(Enum):
        """消息响应状态"""
        Positive = 1
        """正向反馈"""
        Negative = -1
        """负向反馈"""
        Timeout = -2
        """超时反馈"""
        BadConnection = -3
        """连接错误反馈"""
        OtherError = -4
        """其他错误反馈"""
        Null = 0
        """空反馈"""

    class Source(Enum):
        """消息响应来源"""
        Undefined = 0
        """未定义"""
        Server = 1
        """服务器"""
        Peer = 2

    def __init__(self):
        """初始化消息响应"""
        self.content = {}
        """响应内容"""
        self.status = self.Status.Null
        """响应状态"""
        self.source = self.Source.Undefined
        """响应来源"""


class ServerConnection:
    def __init__(self):
        """初始化服务器连接"""
        self.last_response = Response()
        """上一次的消息响应"""
        pass

    def refresh(self) -> Response:
        """刷新连接

        Returns:
            Response: 响应
        """
        pass

    def update_vericode(self, email: str) -> Response:
        """更新验证码并发送邮件
        
        Args:
            email (str): 电子邮件地址
            
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

    def query_friend_list(self) -> Response:
        """请求好友列表

        Returns:
            Response: 响应 (`Response.content['value']` 为好友列表)
        """
        pass

    def find_user(self, user_email: str) -> Response:
        """查找用户

        Args:
            user_email (str): 邮件地址

        Returns:
            Response: 响应 (`Response.status.Negative`)
        """
        pass

    def add_friend(self, friend_email: str) -> Response:
        """添加好友

        Args:
            friend_email (str): _description_

        Returns:
            Response: _description_
        """
        pass

    def delete_friend(self, friend_email: str) -> Response:
        pass

    def start_chat(self, friend_email: str) -> Response:
        pass

    def close(self) -> Response:
        pass


class PeerListener:
    def __init__(self, recv_callback: Callable[[str, float, bytes], None]):
        """_summary_

        Args:
            recv_callback (Callable[[str, float, bytes], None]): _description_
        """
        self.callback = recv_callback
        pass

    def run(self) -> None:
        pass


class PeerSender:
    def __init__(self, server_response: Response):
        self.dest_email: str = None
        self.dest_ip: str = None
        self.dest_port: int = None
        self.last_response = Response()
        pass

    def send(self, message: bytes) -> Response:
        pass

    def close(self) -> Response:
        pass


class Demo:
    def __init__(self):
        self.rcvd = []

    def add(self, email, time, msg):
        self.rcvd.append((email, time, msg))


if __name__ == '__main__':
    demo = Demo()
    pl = PeerListener(demo.add)
    pl.callback('123@abc.com', '100', b'Hello!')
    pl.callback('123@abc.com', '200', b'Hello!')
    pl.callback('123@abc.com', '300', b'Hello!')
    print(demo.rcvd)