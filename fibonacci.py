# -*- encoding:utf-8 -*-
#fib=lambda n:1 if n<=2 else fib(n-1)+fib(n-2)

import time
previous = {1:1L, 2:1L}
def fib(n):
    if previous.has_key(n):
        return previous[n]
    else:
        newValue = fib(n-1) + fib(n-2)
        previous[n] = newValue
        return newValue

def fib1(max):
    n, a, b = 0, 0, 1
    list = []
    while n < max:
        list.append(b)
        a, b = b , a+b
        n += 1
    return list[max-1]

#内存问题，如何能够使内存保持一个常数
class Fab(object):
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1
    def __iter__(self):
        return self
    def next(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a+self.b
            self.n = self.n + 1
            return r
        raise StopIteration()
#for n in Fab(5):
#    print n
    
#使用yield
def fib2(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+b
        n = n + 1
#for n in fib2(5):
#    print n


if __name__ == '__main__':
    #start = time.clock()
    #import profile
    #answer =  fib1(50)
    #end = time.clock()
    #print answer
    
