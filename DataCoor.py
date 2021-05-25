import hashlib
def datacoor(data):
    b = hashlib.sha256()
    b.update(data.encode('utf8'))
    c= b.hexdigest()

    coor_2 = int(c,16) % (2**16)
    coor_1 = int((int(c,16) % (2**32)-coor_2) /(2**16))
    cm = 65536
    # print(coor_2)
    # print(coor_1)
    # print(cm)
    return [coor_1/cm, coor_2/cm]


