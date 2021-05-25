import cuckoofilter
import table_global
import hashutils

class DataCenter(object):
    '''
    数据中心类，每个数据中心直连一个交换机及多个边缘服务器。

    每个数据中心都维护一个域内的布谷鸟哈希表及一个全局的索引（部分）
    '''
    def __init__(self, dc_id, swt_id):
        self.id = dc_id
        self.swt_id = swt_id
        self.table_intra = cuckoofilter.CuckooFilter(capacity=750, bucket_size=4,
                                                     fingerprint_size=1, max_displacements=500)
        self.table_inter = table_global.table_global()

    def lookup_inter(self, item):
        """
        先在域内查找，如果不在域内，则查找全局表
        """
        if self.table_intra.contains(item[0]) is not False:
            # return item + '在该数据中心中，其位于边缘服务器：' + str(self.table_in.contains(item))
            return 1
        elif self.table_inter.lookup(hashutils.fingerprint(item[0], 1)) is not False:
            # return item + '不在该数据中心中，其所在边缘服务器IP为：' + str(self.table_out.lookup(hashutils.fingerprint(item,1)))
            return 2
        else:
            return 3

    def lookup_intra(self, item):
        """
        先在域内查找，如果不在域内，则查找全局表
        """
        if self.table_intra.contains(item) is not False:
            return 1
        else:
            return 3