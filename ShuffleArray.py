import random
count = [0,0,0,0,0,0,0,0,0,0,0,0,0,]
matrix = []
for i in range(13):
    matrix.append(count)

##print matrix[0, 0]
def ShuffleArray(arr, lenth):
    i = lenth
    k = lenth
    if i == 0:
        return
    while i:
        j = random.randint(0, 12) % (i+1)
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp
        i = i - 1
    for elem in arr:
        matrix[elem][k%lenth] += 1
        k += 1

def main():
    for i in range(100000):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        ShuffleArray(arr, 12)

if __name__ == '__main__':
    main()
    for i in matrix:
        print i
