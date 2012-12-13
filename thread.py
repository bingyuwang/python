#-*- encoding:utf-8 -*-
import time
import threading
class mythread(threading.Thread):
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    #ÖØĞ´run·½·¨
    def run(self):
        while not self.thread_stop:
            print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.clock())
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True

def main():
    thread1 = mythread(1, 1)
    thread2 = mythread(2, 2)
    thread1.start()
    thread2.start()
    time.sleep(10)
    thread1.stop()
    thread2.stop()
    return

num = 0
mylock = threading.RLock()
class add_thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name

    def run(self):
        global num
        while True:
            mylock.acquire()
            print 'Thread(%s) locked, num: %d'%(self.t_name, num)
            if num > 4:
                mylock.release()
                print 'thread(%s) released, num: %d' % (self.t_name, num)
                break
            num += 1
            print 'Thread(%s) released, num: %d' % (self.t_name, num)
            mylock.release()

def test():
    thread1 = add_thread('A')
    thread2 = add_thread('B')
    thread1.start()
    thread2.start()

if __name__ == '__main__':
    test()
