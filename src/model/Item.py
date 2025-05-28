from common.Binding import Binding
from component.xml_loader import XMLDATA

class Item:
    def __init__(self, id, count: int = 1):
        self._id = id
        self._count = count
        self._itemCfg = None
        self._width = None
        self._height = None
        self._maxStack = None
        self._quality = None
        self._level = None
        self._binding = None
    
    def __str__(self):
        pass
    
    @property
    def id(self):
        return self._id
    
    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self, count: int):
        if count < 0:
            raise ValueError("Count cannot be negative")
        self._count = count
    
    @property
    def itemCfg(self):
        return XMLDATA.get_item_cfg(self.id)
    
    @property
    def width(self):
        return self.itemCfg.get('width', 1)
    
    @property
    def height(self):
        return self.itemCfg.get('height', 1)
    
    @property
    def maxStack(self):
        return self.itemCfg.get('max_stack', 1)
    
    @property
    def quality(self):
        return self.itemCfg.get('quality', 1)
    
    @property
    def level(self):
        return self.itemCfg.get('level', 1)
    
    @property
    def binding(self):
        return self.itemCfg.get('binding', 0)
    
    @binding.setter
    def binding(self, binding: Binding):
        self._binding = binding.value
    
    