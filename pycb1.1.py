def fun(char):
    return ord(char)

string = "abcde"
result = map(fun, string)
print result
# output: [97, 98, 99, 100, 101]
