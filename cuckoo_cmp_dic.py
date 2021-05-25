# import Data
# import cuckoofilter
# import random
# import time
#
# data_list = {}
# data_num = 2000
# cf = cuckoofilter.CuckooFilter(200,15,1,500)
# search_num = 2000
# num_right = 0
#
# cuc_time_s = time.time()
# for _ in range(data_num):
#     tmp = Data.Data(locate=0,type='intra',num=8,radius=100,id=_)
#     data_list[_] = tmp
#
# for keys in data_list:
#     cf.insert([data_list[keys].value,0])
#
# for _ in range(search_num):
#     index_random = random.randint(0,len(data_list)-1)
#     if cf.contains([data_list[index_random].value,0]):
#         num_right += 1
# cuc_time_e = time.time()
#
# print('cuc_time = '+str(cuc_time_e-cuc_time_s))
#


import switch
i = 1
list = []
print('s%d'%i)
vars()['s%d'%i] = switch.switch([89.24610732,52.84404292],i,i)
list.append(vars()['s%d'%i])
