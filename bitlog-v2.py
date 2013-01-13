# coding:utf-8
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
        super(MainFrame, self).__init__() # ��ʼ��

        self.set_title("BitLog") # ����
        self.set_size_request(250, 100) # ���ڴ�С
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        
        login_btn = gtk.Button("Login")
        login_btn.connect("clicked", self.login)
        logout_btn = gtk.Button("Logout")
        logout_btn.connect("clicked", self.logout)
        setting_btn = gtk.Button("s")
        setting_btn.connect("clicked", self.Se)
        about_btn = gtk.Button("a")
        about_btn.connect("clicked", self.Ab)

        fixed = gtk.Fixed()
        fixed.put(setting_btn, 100,20)
        fixed.put(about_btn, 120, 20)
        fixed.put(login_btn, 20, 40)
        fixed.put(logout_btn, 80, 40)

        self.add(fixed)
        self.show_all()
    
    def login(self, widget):
        signal, info = log_in(user, pswd, sta)
        if signal:
            self.iconify()
        else:
            print info

    def logout(self, widget):
        info  = log_out(user, pswd)
        print info
        
    # Settings
    def Se(self, widget):
        settings()

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

        user_entry = gtk.Entry()
        pswd_entry = gtk.Entry()

        sta_btn = gtk.CheckButton("guojiliuliang") # ��������
        sta_btn.set_active(True)
        sta_btn.connect("clicked", self.sta_change)
        
        save_btn = gtk.Button("Save")
        save_btn.connect("clicked", self.save)
        
        fixed.put(user_entry, 20, 20)
        fixed.put(pswd_entry, 20, 50)
        fixed.put(sta_btn, 20, 80)
        fixed.put(save_btn, 100, 80)

        self.add(fixed)
        self.show_all()
    
    
    def sta_change(self, widget):
        if widget.get_active():
            sta = 0
        else:
            sta = 1

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

# ��¼��ע��
def log_in(user, password, sta):
    #����Cookie��Ϣ
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    #���������MD5����
    a = md5.new(password)
    pswd = a.hexdigest()
    login_pswd = pswd[8:-8]
    
    log_url = 'http://10.0.0.55/cgi-bin/do_login'#post_url
    login_info = {
        'drop' : sta,    #1Ϊ�����������Դ��0Ϊ����ʹ�ù�������
        'n' : 100,     #100Ϊ������½��1Ϊǿ��ע��
        'password' : login_pswd,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(login_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()#��ȡ������Ϣ
    if re.search('[^a-z]',revalue[0:1]): #��½�ɹ�
        return True, 'succeed'
    else:
        return False, revalue

def log_out(user, password):
    log_url = 'http://10.0.0.55/cgi-bin/force_logout'
    logout_info = {
        'drop' : 0,     #1Ϊ�����������Դ��0Ϊ����ʹ�ù�������
        'n' : 1,        #100Ϊ������½��1Ϊǿ��ע��
        'password' : password,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(logout_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()
    return revalue # ����ע�����

MainFrame()
gtk.main()
