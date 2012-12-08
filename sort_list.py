# -*- encoding:utf-8 -*-
#根据第N个元素排序

E=[(1,2,6),(1,3,1),(1,4,5),(2,3,5),(2,5,3),(3,4,5),(3,5,6),(3,6,4),(4,6,2),(5,6,6)]
E.sort(key=lambda d:d[2])
print E

new_E = sorted(E, key = lambda x: x[2])
print new_E
