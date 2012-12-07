def fun2(fun):
    def wrapper():
        print 'hi'
        return fun()
    return wrapper

@fun2

def pri():
    print 'pri'

pri()
