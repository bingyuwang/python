# -*- coding:utf-8 -*-
import Tkinter
import urllib
import urllib2
import cookielib
import md5
import re
import cPickle as pickle
import tkMessageBox as box
import os
import random
def log_in(user, password, sta):
    #处理Cookie信息
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    #把密码进行MD5加密
    a = md5.new(password)
    pswd = a.hexdigest()
    login_pswd = pswd[8:-8]
    
    log_url = 'http://10.0.0.55/cgi-bin/do_login'#post_url
    login_info = {
        'drop' : sta,    #1为仅访问免费资源，0为可以使用国际流量
        'n' : 100,     #100为正常登陆，1为强制注销
        'password' : login_pswd,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(login_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()#读取返回信息
    if re.search('[^a-z]',revalue[0:1]):#登陆成功
        i = random.randint(1,10)
        if i == 1 or i == 2:
            onError(str(i))
        else:
            pass
        root.wm_iconify()#窗口最小化
    else:
        onError(revalue)#弹出错误框

def log_out(user, password):
    log_url = 'http://10.0.0.55/cgi-bin/force_logout'
    logout_info = {
        'drop' : 0,     #1为仅访问免费资源，0为可以使用国际流量
        'n' : 1,        #100为正常登陆，1为强制注销
        'password' : password,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(logout_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()
    onError(revalue)#提示注销结果
    
def onError(case):
    if case == 'username_error':
        box.showerror("ERROR", "尼玛，用户名错误！")
    elif case == 'password_error':
        box.showerror("ERROR","尼玛，密码错误！")
    elif case == 'status_error':
        box.showerror("ERROR","亲，你已经欠费")
    elif case == 'available_error':
        box.showerror("ERROR","账号已进入黑名单，地球很危险，还是回火星吧")
    elif case == 'ip_exist_error':
        box.showerror("ERROR","等会儿，IP还没下线，急什么")
    elif case == 'usernum_error':
        box.showerror("ERROR","骚年，这号有人在登啦")
    elif case == 'online_num__error':
        box.showerror("ERROR","骚年，这号有人在登啦")
    elif case == 'logout_error':
        box.showerror("ERROR","你TMD根本没在线")
    elif case == 'logout_ok':
        box.showerror("OK","注销成功，学术去吧")
    elif case == 'ip_error':
        box.showerror("ERROR","IP好像不对耶")
    elif case == 'notfoundgif':
        box.showerror("ERROR","别给我把gif图标整丢了")
    elif case == '1':
        box.showerror("登陆成功","XX不OO,OO不XX，你懂的")
    elif case == '2':
        box.showerror("登陆成功","网速不给力啊，有木有")
    else:
        box.showerror("ERROR","唔，不知道哪出错了")

class MyDialog:
    def __init__(self, root):
        self.top = Tkinter.Toplevel(root)
        self.top.geometry("280x220+535+260")
        #输入账号
        u = Tkinter.StringVar()
        u.set(user)
        self.user = Tkinter.Entry(self.top, textvariable = u, width = 15)
        userlabel = Tkinter.Label(self.top, width = 12, height = 5, text = u"账号")
        userlabel.grid(row = 0, column = 0)
        self.user.grid(row = 0, column = 1)
        
        #输入密码
        p = Tkinter.StringVar()
        p.set(pswd)
        self.pswd = Tkinter.Entry(self.top, textvariable = p, width = 15)
        pswdlabel = Tkinter.Label(self.top, width = 12, height = 2, text = u"密码")
        pswdlabel.grid(row = 1, column = 0)
        self.pswd.grid(row = 1, column = 1)
        self.pswd['show'] = '*'
        #保存按钮
        save_but = Tkinter.Button(self.top, text = u"保存", command = self.save)
        save_but.grid(row = 2, column = 1, sticky = 'e')
        #是否使用国际流量
        global v
        v = Tkinter.IntVar()
        v.set(sta)
        self.check_but = Tkinter.Checkbutton(self.top, variable = v, width = 12, text = u'仅使用免费流量', command = self.checkbutton)
        self.check_but.grid(row = 2, column = 0)

    def checkbutton(self):#判断是否使用国际流量
        if sta == 0:
            v.set(1)
        else:
            v.set(0)

    def save(self):
        global user
        global pswd
        global sta
        user = self.user.get()
        pswd = self.pswd.get()
        sta = v.get()
        fuser = file('user.pkl','wb+')
        fpswd = file('pswd.pkl','wb+')
        fsta = file('sta.pkl','wb+')
        pickle.dump(user, fuser)
        pickle.dump(pswd, fpswd)
        pickle.dump(sta,fsta)
        self.top.destroy()
    def get(self):
        return self.input

class MyButton():
    def __init__(self, root, type):
        self.root = root
        if type == 0:
            self.button = Tkinter.Button(root,command = self.data, bitmap = 'info', width = 20)
            self.button.pack(side = 'right', anchor = 'ne')
        elif type == 1:
            try:
                global img_left
                img_left = Tkinter.PhotoImage(file = 'up.gif')
                self.button = Tkinter.Button(root, command = self.login, image = img_left, width =200, height = 220)
                self.button.pack(side = 'bottom')
            except:
                onError('notfoundgif')
                os._exit(0)
        elif type == 2:
            try:
                global img_right
                img_right = Tkinter.PhotoImage(file = 'down.gif')
                self.button = Tkinter.Button(root, command = self.logout, image = img_right, width =200, height = 220)
                self.button.pack(side = 'bottom', padx = 10)
            except:
                onError('notfoundgif')
                os._exit(0)
        elif type == 3:
            self.button = Tkinter.Button(root, command = self.aboutdia, bitmap = 'hourglass', width = 20)
            self.button.pack(side = 'right', anchor = 'ne')
    def data(self):
        d = MyDialog(self.root)

    def login(self):
        if user == '' or pswd == '':
            d = MyDialog(self.root)
        else:
            try:
                log_in(user, pswd, sta)
            except:
                onError("url_error")

    def logout(self):
        if user == '' or pswd == '':
            d = MyDialog(self.root)
        else:
            try:
                log_out(user, pswd)
            except:
                onError("url_error")

    #关于框
    def aboutdia(self):
        self.top = Tkinter.Toplevel(root)
        self.top.title("About BitLog")
        self.top.geometry("280x220+535+260")
        about = Tkinter.Message(self.top, text = "\n \n About BitLog\n Version 1.0\n 陈铮 2012\n 关于BitLog http://www.liamchzh.co.cc\n 问题反馈 liamchzh@gmail.com ",
                                width = 280, justify = 'center')
        close_but = Tkinter.Button(self.top, text = u"关闭", command = self.close)
        close_but.pack(side = 'bottom',anchor = 'center')
        about.pack()

    #关闭关于框
    def close(self):
        self.top.destroy()
        
if __name__ == '__main__':
    root = Tkinter.Tk()
    root.geometry("280x440+535+150")
    root.title("BitLog")
    global user
    global pswd
    global sta
    try:
        fuser = file('user.pkl','rb+')
        fpswd = file('pswd.pkl','rb+')
        fsta = file('sta.pkl','rb+')
        user = pickle.load(fuser)
        pswd = pickle.load(fpswd)
        sta = pickle.load(fsta)
    except:
        fuser = file('user.pkl','wb+')
        fpswd = file('pswd.pkl','wb+')
        fsta = file('sta.pkl','wb+')
        print 'user&pswd can\'t be read'
        user = ''
        pswd = ''
        sta = 0
    MyButton(root, 3)#关于页面
    MyButton(root, 0)#修改账号密码
    MyButton(root, 2)#注销按钮
    MyButton(root, 1)#登陆按钮
    root.mainloop()
