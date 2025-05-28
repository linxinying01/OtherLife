"""
    背包系统
    
    数据结构：二维矩阵
"""

from model.Item import Item
from loguru import logger


class Backpack:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]  # 初始化背包网格，0表示空位
        self.items = {}  # 存储物品信息 {idx: Item}
        
    def get_item(self, row, col):
        self.items.get((row - 1, col - 1), None)
        
    def canPlaceWithPosition(self, item, row, col):
        """判断能否将该物品放入背包指定位置"""
        # 同物品要考虑叠加
        # 不同物品直接失败
        if not isinstance(item, Item):
            logger.warning("item must be an instance of Item")
            return False
        if row <= 0 or row <= 0:
            return False
        if row + item.height - 1 > self.rows or col + item.width - 1 > self.cols:
            return False
        old_item = self.get_item(row, col)
        if old_item is not None:
            if old_item.id != item.id:
                return False
            else:
                if old_item.count + item.count > old_item.maxStack:
                    return False
                return True
        else:
            if item.count > item.maxStack:
                return False
            for r in range(row - 1, row + item.height - 1):
                for c in range(col - 1, col + item.width - 1):
                    if self.grid[r][c] != 0:
                        return False
            return True
        
    
    def canPlaceWithoutPosition(self, item):
        """判断能否将该物品放入背包任意位置"""
        pass
    
    def placeWithPosition(self, item):
        pass
    
    def placeWithoutPosition(self, item):
        pass
    
    def remove(self, item_id, count=1):
        pass
    
    def display(self):
        pass
    

if __name__ == '__main__':
    bp = Backpack(5, 10)
    print(bp.grid)