#fib=lambda n:1 if n<=2 else fib(n-1)+fib(n-2)
#print fib(1)
import time
previous = {1:1L, 2:1L}
def fib(n):
    if previous.has_key(n):
        return previous[n]
    else:
        newValue = fib(n-1) + fib(n-2)
        previous[n] = newValue
        return newValue

if __name__ == '__main__':
    start = time.clock()
    import profile
    answer =  fib(50)
    end = time.clock()
    print answer
    print start
    print end
    
    
