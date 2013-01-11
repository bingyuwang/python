# coding:utf-8
import gtk
class MainFrame(gtk.Window):
    def __init__(self):
        super(MainFrame, self).__init__() #初始化

        
        self.set_title("BitLog") #标题
        self.set_size_request(250, 100) #窗口大小
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        """
        vbox = gtk.VBox(False, 5)
        hbox = gtk.HBox(True, 3)

        valign = gtk.Alignment(0,1,0,0)
        vbox.pack_start(valign)

        login_btn = gtk.Button("Login")
        login_btn.set_size_request(70,30)
        logout_btn = gtk.Button("Logout")

        hbox.add(login_btn)
        hbox.add(logout_btn)

        halign = gtk.Alignment(1,0,0,0)
        halign.add(hbox)
        
        vbox.pack_start(halign, False, False, 3)

        self.add(vbox)
        """
        login_btn = gtk.Button("Login")
        logout_btn = gtk.Button("Logout")
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

    def Se(self, widget):
        setting = gtk.Window()
        setting.set_title(u"Settings")

        fixed = gtk.Fixed()

        user_entry = gtk.Entry()
        pswd_entry = gtk.Entry()
        fixed.put(user_entry, 20, 20)
        fixed.put(pswd_entry, 20, 50)

        setting.add(fixed)
        setting.show_all()

    def Ab(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("BitLog")
        about.set_version("2.0")
        about.set_copyright("(c) Liam")
        about.set_comments(u"BitLog is a ...")
        about.set_website("http://liamchzh.com")
        about.run()
        about.destroy()

MainFrame()
gtk.main()
