import random
import bucket
import exceptions
import hashutils

class CuckooFilter(object):
    """
    布谷鸟哈希表类.

    Implements insert, delete and contains operations for the filter.
    """

    def __init__(self, capacity, bucket_size=4, fingerprint_size=1,
                 max_displacements=500):
        """
        Initialize CuckooFilter object.

        :param capacity: Size of the Cuckoo Filter
        :param bucket_size: Number of entries in a bucket
        :param fingerprint_size: Fingerprint size in bytes
        :param max_displacements: Maximum number of evictions before filter is
        considered full
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.max_displacements = max_displacements
        self.buckets = [bucket.Bucket(size=bucket_size)
                        for _ in range(self.capacity)]
        self.size = 0

    def __repr__(self):
        return '<CuckooFilter: capacity=' + str(self.capacity) + \
               ', size=' + str(self.size) + ', fingerprint size=' + \
               str(self.fingerprint_size) + ' byte(s)>'

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return self.contains(item)

    def _get_index(self, item):
        """
        此item为列表：[项目,es_id]
        """
        index = hashutils.hash_code(item[0]) % self.capacity
        return index

    def _get_alternate_index(self, index, fingerprint):
        alt_index = (index ^ hashutils.hash_code(fingerprint)) % self.capacity
        return alt_index

    def insert(self, item):
        """
        Insert an item into the filter.
        插入的时候，item为[项目,es_id]

        :param item: Item to be inserted.
        :return: True if insert is successful; CuckooFilterFullException if
        filter is full.
        """
        fingerprint = hashutils.fingerprint(item[0], self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)

        if self.buckets[i].insert([fingerprint,item[1]]):
            self.size += 1
            # print("插入到了i："+str(i))
            return True
        elif self.buckets[j].insert([fingerprint,item[1]]):
            self.size += 1
            # print("插入到了j："+str(j))
            return True


        for _ in range(self.max_displacements):
            eviction_index = random.choice([i, j])
            f = self.buckets[eviction_index].swap([fingerprint,item[1]])
            eviction_index_1 = self._get_alternate_index(eviction_index, f[0])
            if self.buckets[eviction_index_1].insert(f):
                self.size += 1
                return True

        # Filter is full
        raise exceptions.CuckooFilterFullException('Insert operation failed. '
                                                   'Filter is full.')

    def contains(self, item):
        """
        Check if the filter contains the item.
        此item为[项目,0]
        :param item: Item to check its presence in the filter.
        :return: 如果在cuckoo中，返回其存储的es_id，若不在，则返回False
        """

        fingerprint = hashutils.fingerprint(item[0], self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)
        # print('bucket before:'+str(self.buckets[i].bucket))
        list_i = []
        list_j = []
        for _ in range(len(self.buckets[i].bucket)):
            # print('length:'+str(len(self.buckets[i])))
            # print(self.buckets[i].bucket[_][0])
            list_i.append(self.buckets[i].bucket[_][0])
        for _ in range(len(self.buckets[j].bucket)):
            # print('length:'+str(len(self.buckets[j])))
            list_j.append(self.buckets[j].bucket[_][0])
        # print(list_i)
        # print(list_j)
        if fingerprint in list_i:
            # print(fingerprint)
            # print('index:' + str(list_i.index(fingerprint)))
            # print('bucket after:'+str(self.buckets[i].bucket))
            return self.buckets[i].bucket[list_i.index(fingerprint)][-1]
        elif fingerprint in list_j:
            # print(self.buckets[j].bucket)
            return self.buckets[j].bucket[list_j.index(fingerprint)][-1]
        else:
            return False

    def delete(self, item):
        """
        Delete an item from the filter.

        To delete an item safely, it must have been previously inserted.
        Otherwise, deleting a non-inserted item might unintentionally remove
        a real, different item that happens to share the same fingerprint.
        此item为列表：[项目，es_id]
        :param item: Item to delete from the filter.
        :return: True, if item is found and deleted; False, otherwise.
        """
        fingerprint = hashutils.fingerprint(item[0], size=self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)
        if self.buckets[i].delete([fingerprint,item[1]]) \
                or self.buckets[j].delete([fingerprint,item[1]]):
            self.size -= 1
            return True
        return False


