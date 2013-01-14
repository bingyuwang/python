# coding:utf-8

import pygtk
import gtk
import urllib
import urllib2
import cookielib
import md5
import re
import os
import cPickle as pickle

class MainFrame(gtk.Window):
    def __init__(self):
        super(MainFrame, self).__init__() # 初始化

        self.set_title("BitLog") # 标题
        self.set_size_request(250, 100) # 窗口大小
        self.set_position(gtk.WIN_POS_CENTER) # 窗口位置
        self.connect("destroy", gtk.main_quit)
        
        login_img = gtk.Image()
        login_img.set_from_file("login.png")
        logout_img = gtk.Image()
        logout_img.set_from_file("login.png")
        setting_img = gtk.Image()
        setting_img.set_from_file("setting.png")
        about_img = gtk.Image()
        about_img.set_from_file("about.png")
        
        login_btn = gtk.Button() #登录按钮
        login_btn.set_image(login_img)
        login_btn.connect("clicked", self.login)
        login_btn.set_tooltip_text(u"登录")

        logout_btn = gtk.Button() #注销按钮
        logout_btn.set_image(logout_img)
        logout_btn.connect("clicked", self.logout)
        logout_btn.set_tooltip_text(u"注销")

        setting_btn = gtk.Button()
        setting_btn.set_image(setting_img)
        setting_btn.connect("clicked", self.Se)
        setting_btn.set_tooltip_text(u"设置")

        about_btn = gtk.Button()
        about_btn.set_image(about_img)
        about_btn.connect("clicked", self.Ab)
        about_btn.set_tooltip_text("关于")

        fixed = gtk.Fixed()
        fixed.put(setting_btn, 100,20)
        fixed.put(about_btn, 140, 20)
        fixed.put(login_btn, 20, 50)
        fixed.put(logout_btn, 80, 50)

        self.add(fixed)
        self.show_all()

        global user, pswd, sta
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
            user = ''
            pswd = ''
            sta = 0
    
    def login(self, widget):
        signal, info = log_in(user, pswd, sta)
        if signal:
            self.iconify()
        else:
            self.Message(self, info)

    def logout(self, widget):
        info  = log_out(user, pswd)
        self.Message(self, info)
        
    # Settings
    def Se(self, widget):
        settings()

    # 消息框
    def Message(self, widget, case):
        if case == 'username_error':
            info = u"用户名错误"
        elif case == 'password_error':
            info = u"密码错误"
        elif case == 'status_error':
            info = u"用户已欠费"
        elif case == 'available_error':
            info = u"用户已禁用"
        elif case == 'ip_exist_error':
            info = u"IP尚未下线，请稍后"
        elif case == 'usernum_error':
            info = u"用户数已达上限"
        elif case == 'online_num__error':
            info = u"登陆人数超过限额"
        elif case == 'logout_error':
            info = u"您不在线上"
        elif case == 'logout_ok':
            info = u"注销成功"
        elif case == 'ip_error':
            info = u"您的IP不合法"
        else:
            info = u"暂时无法完成操作"

        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, info)
        md.run()
        md.destroy()
        
    # About
    def Ab(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("BitLog")
        about.set_version("2.0")
        about.set_copyright("(c) Liam")
        about.set_comments(u"BitLog is a ...")
        about.set_website("http://liamchzh.com")
        about.run()
        about.destroy()

class settings(gtk.Window):
    def __init__(self):
        super(settings, self).__init__()
        
        self.set_title("Settings")
        self.set_default_size(250, 200)
        self.set_position(gtk.WIN_POS_CENTER)
        
        fixed = gtk.Fixed()

        global user_entry, pswd_entry, sta
        sta = 1

        user_entry = gtk.Entry(40)
        pswd_entry = gtk.Entry(40)
        pswd_entry.set_visibility(False)# 密码文本框字符不可见
        user_entry.set_max_length(20)
        pswd_entry.set_max_length(20)

        sta_btn = gtk.CheckButton(u"仅使用免费流量") # 是否国际流量
        sta_btn.connect("clicked", self.sta_change)
        
        save_btn = gtk.Button("Save")
        save_btn.connect("clicked", self.save)
        
        fixed.put(user_entry, 20, 20)
        fixed.put(pswd_entry, 20, 50)
        fixed.put(sta_btn, 20, 80)
        fixed.put(save_btn, 100, 80)

        self.add(fixed)
        self.show_all()
    
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
            user = ''
            pswd = ''
            sta = 0

        user_entry.set_text(user)
        pswd_entry.set_text(pswd)
        if sta:
            sta_btn.set_active(True)

    def sta_change(self, widget):
        global sta
        if widget.get_active():
            sta = 1
        else:
            sta = 0

    def save(self, widget):
        global user, pswd, sta
        user = user_entry.get_text()
        pswd = pswd_entry.get_text()
        fuser = file('user.pkl','wb+')
        fpswd = file('pswd.pkl','wb+')
        fsta = file('sta.pkl','wb+')
        pickle.dump(user, fuser)
        pickle.dump(pswd, fpswd)
        pickle.dump(sta,fsta)
        self.destroy()

# 登录和注销
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
    if re.search('[^a-z]',revalue[0:1]): #登陆成功
        return True, 'succeed'
    else:
        return False, revalue

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
    return revalue # 返回注销结果

if __name__ == '__main__':
    MainFrame()
    gtk.main()

