import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_canPlace():
    from component import xml_loader
    xml_loader.load_xmls("data/xml")
    from src.model.Backpack import Backpack
    from src.model.Item import Item

    bp = Backpack(10, 10)
    item = Item(10001, 10000)

    assert bp.canPlaceWithPosition(item, 1, 1) is True