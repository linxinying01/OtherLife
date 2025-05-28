from enum import Enum


class Vocation(Enum):
    """职业枚举类"""
    WARRIOR = 1
    MAGE = 2
    ROGUE = 3
    PRIEST = 4
    HUNTER = 5
    PALADIN = 6
    SHAMAN = 7
    WARLOCK = 8

    @classmethod
    def get_vocation_name(cls, vocation_id):
        """根据职业ID获取职业名称"""
        return cls(vocation_id).name if vocation_id in cls._value2member_map_ else None
