import random
matrix = [([0] * 13) for i in range(13)]
def ShuffleArray(arr, lenth):
    i = lenth
    if i == 0:
        return
    while i:
        j = random.randint(0, 12) % (i+1)
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp
        i = i - 1
    k = 0
    for elem in arr:
        matrix[int(elem)][k] += 1
        k += 1

def main():
    for i in range(1000000):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        ShuffleArray(arr, 12)

if __name__ == '__main__':
    main()
    for i in matrix:
        print i
