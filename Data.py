import random
import string
import DataCoor
class Data(object):
    def __init__(self, id, locate, type, num, radius):
        self.id = id
        self.value = None
        self.locate = locate
        self.type = type
        self.coordinate = None
        self.ValueGive(num, radius)


    def ValueGive(self, num, radius):
        self.value = ''.join(random.sample(string.ascii_letters + string.digits, num))
        if self.type == 'inter':
            a,b = DataCoor.datacoor(self.value)
            self.coordinate = [a*radius,b*radius]
        else:
            self.coordinate = self.locate

# a = Data(201,'intra')
# a.ValueGive(8)
#
# print(a.value)
# print(a.locate)
# print(a.type)
# print(a.coor)