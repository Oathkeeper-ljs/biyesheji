import cuckoofilter
from pybloom import pybloom
import random
import string
import time

def test(cishu):
    test_list = []
    data_num = 3000
    search_num = cishu
    right_cf = 0
    right_bf = 0
    for _ in range(data_num):
        a = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        test_list.append(a)

    # print(test_list)

    cf = cuckoofilter.CuckooFilter(capacity=1000,bucket_size=20,fingerprint_size=1,max_displacements=500)

    for _ in range(data_num):
       cf.insert([test_list[_],0])

    cf_time_start = time.time()
    for _ in range(search_num):
        b =  ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if ((b in test_list) and (cf.contains([b,0])) is not False) or ((b not in test_list) and (cf.contains([b,0]) is False)):
            right_cf += 1
    cf_time_end = time.time()

    bf = pybloom.BloomFilter(capacity=6000,error_rate=0.03125)
    for _ in range(data_num):
        bf.add(test_list[_],skip_check=True)

    bf_time_start = time.time()
    for _ in range(search_num):
        b =  ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if ((b in test_list) and (b in bf)) or ((b not in test_list) and (b not in bf)):
            right_bf += 1
    bf_time_end = time.time()

    print(right_cf)
    print(right_bf)
    print('cf time:'+'%s'%(cf_time_end-cf_time_start))
    print('bf time:'+'%s'%(bf_time_end-bf_time_start))
    return cf_time_end-cf_time_start

count = 0
flag = 0
delay_time = 0
canshu = 1000
list = []
for _ in range(2):

    for loop in range(100):
        if flag == 10:
            break
        else:
            print('flag=%d'%flag)
            print(loop)
            try:
                tmp = test(canshu*(_+1))
                print('time:%s'%tmp)
                count += tmp
                flag += 1
            except:
                pass
    flag = 0
    print('average time is:'+str(count/10))
    list.append(count/10)
    count = 0

