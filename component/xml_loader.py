from datetime import datetime
from loguru import logger
import os
from typing import Any, Dict, Optional
from xml.etree import ElementTree as ET


def format_xml(xml):
    rst = {}
    for k, v in xml.items():
        v_formated = _format_xml_row(v)
        if is_number(k):
            rst[int(k)] = v_formated
        else:
            rst[k] = v_formated
    return rst


# 格式化xml一行数据
def _format_xml_row(row):
    row_formated = {}
    for k, v in row.items():
        k_formated, v_formated = _format_key_value(k, v)
        row_formated[k_formated] = v_formated
    return row_formated


# 格式化xml字段
def _format_key_value(k, v):
    if len(k) <= 2:
        return k, v
    suffix = k[-2:]
    k = k[:len(k) - 2]

    # 兼容字段内容为空
    if not v:
        return k, v

    # print(k, v)

    match suffix:
        case '_i':
            vv = int(v) if is_number(v) else v
            return k, vv
        case '_d':
            vv = int(v) if is_number(v) else v
            return k, vv
        case '_f':
            vv = int(v) if is_number(v) else v
            return k, vv
        case '_s':
            return k, v
        case '_l':
            # 1,2,3
            t = v.split(',')
            rst = []
            for i in t:
                ii = int(i) if is_number(i) else i
                rst.append(ii)
            return k, rst
        case '_k':
            # 1,2,3
            t = v.split(',')
            tmp = {}
            for i in t:
                if is_number(i):
                    tmp[int(i)] = 1
                else:
                    tmp[i] = 1
            return k, tmp
        case '_t':
            # 00:00:00
            t = v.split(':')
            sec = 0
            for i in t:
                if is_number(i):
                    sec = int(i) + sec * 60
            return k, sec
        case '_y':
            # 2014-01-25 0:12:00
            t = v.split(' ')
            t1 = t[0].split('-')
            t11 = []
            for i in t1:
                t11.append(int(i))
            t2 = t[1].split(':')
            t22 = []
            for i in t2:
                t22.append(int(i))
            tt = int(datetime(*t11, *t22).timestamp())
            return k, tt
        case '_m':
            # k:v;k2:v2
            rst = {}
            tmp = v.split(';')
            for vv in tmp:
                tmp2 = vv.split(':')
                kk = int(tmp2[0]) if is_number(tmp2[0]) else tmp2[0]
                vv = int(tmp2[1]) if is_number(tmp2[1]) else tmp2[1]
                rst[kk] = vv
            return k, rst
        case '_n':
            # k:v1,v2,...;k2:v1,v2,...
            rst = {}
            tmp = v.split(';')
            for vv in tmp:
                tmp2 = vv.split(':')
                kk = int(tmp2[0]) if is_number(tmp2[0]) else tmp2[0]
                rst2 = []
                tmp3 = tmp2[1].split(',')
                for i in tmp3:
                    tmp4 = int(i) if is_number(i) else i
                    rst2.append(tmp4)
                rst[kk] = rst2
            return k, rst
        case _:
            return k, v


def is_number(s: str) -> bool:
    if not s:
        return False
    if s[0] == '-':
        return s[1:].isdigit()
    return s.isdigit()


def read_xml_by_one_key(fn: str, key: str, is_delete_zero: bool) -> dict:
    data = {}
    tree = ET.parse(fn)
    root = tree.getroot()
    for child in root:
        row = {}
        row_key = None
        for child1 in child:
            if child1.tag == key:
                row_key = child1.text
            row[child1.tag] = child1.text
        data[row_key] = row
    if is_delete_zero and "0" in data:
        del data["0"]
    data_formated = format_xml(data)
    return data_formated


def read_xml_by_two_key(fn: str, key1: str, key2: str, is_delete_zero: bool) -> dict:
    tree = ET.parse(fn)
    root = tree.getroot()
    data = {}
    src_data = []
    for child in root:
        row = {}
        can_append = True
        for child1 in child:
            row[child1.tag] = child1.text
            if child.tag == 'id_i' and is_delete_zero:
                can_append = False
        if can_append:
            src_data.append(row)
    key1 = key1[:-2]
    key2 = key2[:-2]
    for row in src_data:
        row_formated = _format_xml_row(row)
        v1 = row_formated[key1]
        v2 = row_formated[key2]
        data[v1] = {} if v1 not in data else data[v1]
        data[v1][v2] = row_formated
    return data


class XmlLoader:
    _instance = None
    _loaded = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _init_data(self, xml_path):
        if not self._loaded:
            self.xml_path = xml_path
            self.item_datas = {}  # 所有物品配置统一存放
            self.other_datas = {}
            self._one_key_xmls = [
                # [文件名， 键名, 是否删除0值, 别名，是否是物品数据]
                ['misc.xml', 'id_i', True, None, True],
                ['weapon.xml', 'id_i', True, None, True],
                ['armor.xml', 'id_i', True, None, True],
            ]
            self._two_key_xmls = [
                # [文件名, 键名1, 键名2, 是否删除0值, 别名]
                # ["itemratio.xml", "Uber_i", "Class_Specific_i", True],
            ]
            self._init_xmls()
            self._loaded = True

    def _init_xmls(self):
        for xml_cfg in self._one_key_xmls:
            logger.debug(xml_cfg)
            fn, key, is_delete_zero, fn_alias, is_item_data = xml_cfg
            file_path = os.path.join(self.xml_path, fn)
            if fn_alias is not None:
                fn = fn_alias
            data = read_xml_by_one_key(file_path, key, is_delete_zero)
            if is_item_data:
                for item_id, item_data in data.items():
                    self.item_datas[item_id] = item_data
            else:
                self.other_datas[fn] = data

        for xml_cfg in self._two_key_xmls:
            fn = os.path.join(self.xml_path, xml_cfg[0])
            key1 = xml_cfg[1]
            key2 = xml_cfg[2]
            is_delete_zero = xml_cfg[3]
            fn_alias = xml_cfg[4] if len(xml_cfg) >= 5 else xml_cfg[0]
            data = read_xml_by_two_key(fn, key1, key2, is_delete_zero)
            self.other_datas[fn_alias] = data

    def get_xml(self, xml_name: str) -> dict:
        if xml_name in self.item_datas:
            return self.item_datas[xml_name]
        elif xml_name in self.other_datas:
            return self.other_datas[xml_name]
        else:
            return dict()
         
    def get_data_by_key(self, xml_name: str, key: int) -> dict:
        if xml_name not in self.other_datas:
            return dict()
        if key not in self.other_datas[xml_name]:
            return dict()
        return self.other_datas[xml_name][key]

    def get_data_by_two_key(self, xml_name: str, key1: int, key2: int) -> dict:
        if xml_name not in self.other_datas:
            return dict()
        if key1 not in self.other_datas[xml_name]:
            return dict()
        if key2 not in self.other_datas[xml_name][key1]:
            return dict()
        return self.other_datas[xml_name][key1][key2]

    def get_item_cfg(self, item_id: int) -> Optional[Dict[str, Any]]:
        if item_id in self.item_datas:
            return self.item_datas[item_id]
        else:
            return dict()


# 全局实例
XMLDATA = XmlLoader()


def load_xmls(xml_path: str):
    global XMLDATA
    XMLDATA._init_data(xml_path)


if __name__ == '__main__':
    load_xmls("data/xml")

    print(XMLDATA.get_item_xml_data(20001))
