class table_global(object):
    '''
    全局索引的表，数据结构为字典
    格式为：key+address
    key = fingerprint
    address = address(es) 可以存储es的IP地址
    '''

    def __init__(self):
        self.table = {}

    def contains(self, key):
        '''
        判断key是否已经存在于table中
        '''
        flag = self.table.get(key,0)
        if flag != 0:
            return True
        else:
            return False

    def insert(self, key, address):
        '''
        将key：address插入table
        若本就存在key值，将address加入到列表之后
        反之，直接添加
        '''
        if self.contains(key):
            self.table[key].append(address)
        else:
            self.table[key] = [address]

    def lookup(self, key):
        '''
        查找，返回所有的value
        没找到返回False
        '''
        if self.contains(key):
            return self.table[key]
        else:
            return False

    def delete(self, key, address):
        if self.contains(key):
            if self.table[key]==address:
                self.table.pop(key)
                return True
            elif self.table[key]!=address and address in self.table[key]:
                self.table[key].remove(address)
                return True
            else:
                return False
        else:
            return False
