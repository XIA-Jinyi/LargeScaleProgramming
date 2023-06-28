import re
import control
import page_error
import page_finishi_loging


def validate_inputs(ID, name, pw, repw, code):
    # 检测ID是否为邮箱格式
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', ID):
        return 1

    # 检测name是否只包含大小写字母和数字
    if not re.match(r'^[a-zA-Z0-9]+$', name):
        return 1

    # 检测pw和repw是否相等
    if  pw != repw:
        return 1

    # 检测code是否为非空字符串
    if not code:
        return 1

    return 0