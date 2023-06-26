from enum import Enum


class User:
    """用户"""

    class Status(Enum):
        """用户在线状态"""
        Unknown = 0x00
        Online = 0x01
        Offline = 0x02
        
    def __init__(self):
        """初始化用户"""
        self.username: str = None
        """用户名"""
        self.email: str = None
        """邮件地址"""
        self.status = self.Status.Unknown
        """在线状态"""


class Message:
    """消息"""

    def __init__(self):
        """初始化消息"""
        self.attributes = {}
        """消息属性"""
        self.content: bytes = None
        """消息内容"""


class Response:
    """消息响应"""

    class Status(Enum):
        """消息响应状态"""
        Positive = 0x01
        """正向反馈"""
        PositiveClose = 0x11
        """关闭连接（正向反馈）"""
        Negative = 0x02
        """负向反馈"""
        NegativeClose = 0x12
        """关闭连接（负向反馈）"""
        Timeout = 0xf1
        """超时反馈"""
        BadConnection = 0xf2
        """连接错误反馈"""
        OtherError = 0xf3
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
        """同伴"""
        Client = 3
        """客户端"""

    def __init__(self):
        """初始化消息响应"""
        self.content = {}
        """响应内容"""
        self.status = self.Status.Null
        """响应状态"""
        self.source = self.Source.Undefined
        """响应来源"""
        