# -*- coding:utf-8 -*-

array = [0, 0, 0]
matrix = [array*3]
print matrix
##[[0,0,0,0,0,0,0,0,0]]

array = [0, 0, 0]
matrix = [array] * 3
print matrix
##[[0, 0, 0], [0, 0, 0], [0, 0, 0]]

array = [0, 0, 0]
matrix = [array] * 3
matrix[0][1] = 1
print matrix
##[[0, 1, 0], [0, 1, 0], [0, 1, 0]]

array = [0, 0, 0]
matrix = [array for i in range(3)]
matrix[0][1] = 1
print matrix
##[[0, 1, 0], [0, 1, 0], [0, 1, 0]]

##直接定义
matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
matrix[0][1] = 1
print matrix
##[[0, 1, 0], [0, 0, 0], [0, 0, 0]]

##间接定义
matrix = [[0 for i in range(3)] for i in range(3)]
matrix[0][1] = 1
print matrix
##[[0, 1, 0], [0, 0, 0], [0, 0, 0]]

##以下也是不对的
matrix = [[0] * 3] * 3
matrix[0][1] = 1
print matrix
##[[0, 1, 0], [0, 1, 0], [0, 1, 0]]
