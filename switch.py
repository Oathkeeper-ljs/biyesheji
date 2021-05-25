import Data
class switch(object):
    def __init__(self, locate, swt_id, dc_id):
        self.coor = locate
        self.id = swt_id
        self.directDC = dc_id
        self.table = {}
        """
        转发表的格式为：
        key        value
        swt_id     locate
        """
    def forward(self, data):
        min = (data.coordinate[0]-self.coor[0])**2+(data.coordinate[1]-self.coor[1])**2
        swt_id = self.id
        for keys in self.table:
            dis = (data.coordinate[0]-self.table[keys][0])**2+(data.coordinate[1]-self.table[keys][1])**2
            if dis < min:
                min = dis
                swt_id = keys
        return swt_id

    # 交换机转发表的建立交给主函数做，这样一次Delaunay三角的遍历
    # 即可实现所有交换机转发表的建立
    #def TableCreate(self):

# a = switch([89.24610732,52.84404292],1,2)
# a.table[2] = [69.02110118,50.92382399]
# a.table[4] = [80.74402724,19.95819842]
# a.table[3] = [27.74042455,54.59022338]
# print(a.table)
#
# b = Data.Data([29.13278894,62.08606927],'inter',8)
#
# print(a.forward(b))

"""
switch_coor =
[[89.24610732 52.84404292]
 [27.74042455 54.59022338]
[69.02110118 50.92382399]
[80.74402724 19.95819842]
[ 5.64138149 27.78864018]
[14.18071462 76.65735669]
[44.54071223 63.07833981]
[86.50034257 75.47949493]
[38.57618633  9.46803238]
[29.13278894 62.08606927]]

delaunay triangels:
[(3, 0, 2), (5, 4, 1), (6, 1, 2), (7, 5, 6), (7, 6, 2),
(7, 2, 0), (8, 3, 2), (8, 2, 1), (8, 1, 4), (9, 5, 1), (9, 1, 6), (9, 6, 5)]

"""

