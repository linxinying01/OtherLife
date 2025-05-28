from enum import Enum


class Binding(Enum):
    ROLE = 1  # 角色绑定
    ACCOUNT = 2  # 账号绑定
    DEAL = 3  # 交易绑定
    EMPTY = 4  # 不绑定