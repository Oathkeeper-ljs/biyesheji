import switch
import Data
import hashutils
"""
由Delaunay三角创建swt的转发表
"""
def table_create(triangle_list, swt_list):
    for _ in range(len(triangle_list)):
        a = triangle_list[_][0]
        b = triangle_list[_][1]
        c = triangle_list[_][2]
        swt_list[a].table[b] = swt_list[b].coor
        swt_list[a].table[c] = swt_list[c].coor
        swt_list[b].table[a] = swt_list[a].coor
        swt_list[b].table[c] = swt_list[c].coor
        swt_list[c].table[b] = swt_list[b].coor
        swt_list[c].table[a] = swt_list[a].coor

"""
数据索引发布，计算该数据距离所有swt的距离，返回距离最小的swt直连的DC_id
"""
def data_publish(swt_list,data):
    for _ in range(len(swt_list)):
        min = 30000
        for keys in swt_list:
            dis = (data.coordinate[0]-swt_list[keys].coor[0])**2+(data.coordinate[1]-swt_list[keys].coor[1])**2
            if dis < min:
                min = dis
                swt_id = keys
        dc = swt_list[swt_id].directDC
        return dc

"""
域内查找
:param 想要查找的数据的实体，及执行该查找动作的dc_id
:return 返回查找到的存储在该dc上的es_id 
"""
def search_intra(Data, dc_id, dc_list):
    if dc_list[dc_id].lookup_intra([Data.value,0]) != 3:
        return True
    else:
        return False

"""
域间查找
从任一DC进入，交给其直连的交换机，交换机贪婪转发，直到到达距离数据点最近的交换机，
该交换机将请求发给直连的DC，DC查找全局表，给出结果。
"""
def search_inter(Data, dc_id_random, dc_list, swt_list):
    swt_id = dc_list[dc_id_random].swt_id
    count = 0
    while swt_list[swt_id].forward(Data) != swt_id:
        swt_id = swt_list[swt_id].forward(Data)
        count += 1
        # print(swt_id)
    fingerprint = hashutils.fingerprint(Data.value,1)
    if dc_list[swt_list[swt_id].directDC].table_inter.lookup(fingerprint):
        return [True,count]
    else:
        return False