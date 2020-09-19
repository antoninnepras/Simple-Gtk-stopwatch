import threading
from time import sleep,time,ctime
import gi
from playsound import playsound
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from os import system

openClassic = False

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simple stopwatch")
        self.set_icon_from_file("images/icon.png")
        self.set_resizable(False)
        self.connect("destroy",self.stop_all)
        #fonts
        font1 = Pango.FontDescription("DejaVu 20")

        #stopwatch
        self.stopwatch_label1 = Gtk.Label(label="STOPWATCH")
        self.stopwatch_label1.set_width_chars(60)
        self.button1 = Gtk.Button(label="START")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.button1.override_font(font1)

        self.button2 = Gtk.Button(label="STOP")
        self.button2.set_sensitive(False)
        self.button2.connect("clicked", self.on_button2_clicked)
        self.button2.override_font(font1)

        self.stopwatch_label = Gtk.Label(label=("STOPWATCH"))
        self.stopwatch_label.override_font(font1)

        #timer
        self.timer_label = Gtk.Label(label="TIMER")
        self.timer_label.set_width_chars(60)
        timer_time=0

        self.timer_entry = Gtk.Entry()
        self.timer_entry.set_placeholder_text("SET TIME")
        self.timer_entry.set_alignment(0.5)
        self.timer_entry.override_font(font1)
        self.timer_entry.connect("activate",self.start_timer)

        self.timer_button = Gtk.Button(label="START TIMER")
        self.timer_button.connect("clicked", self.start_timer)
        self.timer_button.override_font(font1)

        self.timer_stop_button = Gtk.Button(label="STOP TIMER")
        self.timer_stop_button.connect("clicked", self.stop_timer)
        self.timer_stop_button.set_sensitive(False)
        self.timer_stop_button.override_font(font1)

        self.timer_remaining_time_label = Gtk.Label(label="NOT STARTED")
        self.timer_remaining_time_label.override_font(font1)

        #clock
        self.clock_label1 = Gtk.Label(label="CLOCK")
        self.clock_label1.set_width_chars(60)
        self.clock_label = Gtk.Label(label="TIME")
        self.clock_label.override_font(font1)
        self.t3=threading.Thread(target=self.clock)
        self.t3.start()

        #grids
        self.clockGrid = Gtk.Grid()
        self.clockGrid.set_row_spacing(10)
        self.clockGrid.set_column_spacing(10)
        self.clockGrid.attach(self.clock_label1,0,0,2,1)
        self.clockGrid.attach(self.clock_label,0,1,2,1)

        self.stopWatchGrid = Gtk.Grid()
        self.stopWatchGrid.attach(self.stopwatch_label1,0,0,2,1)
        self.stopWatchGrid.attach(self.button1,0,1,1,1)
        self.stopWatchGrid.attach(self.button2, 0,2,1,1)
        self.stopWatchGrid.attach(self.stopwatch_label, 1,1,1,2)

        self.timerGrid = Gtk.Grid()
        self.timerGrid.attach(self.timer_label,0,0,2,1)
        self.timerGrid.attach(self.timer_entry,0,1,1,1)
        self.timerGrid.attach(self.timer_remaining_time_label, 1,1,1,1)
        self.timerGrid.attach(self.timer_button,0,2,1,1)
        self.timerGrid.attach(self.timer_stop_button,1,2,1,1)

        #stacks
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        self.stack.add_titled(self.clockGrid,"clockGrid","Clock")
        self.stack.add_titled(self.stopWatchGrid,"stopWatchGrid","Stopwatch")
        self.stack.add_titled(self.timerGrid, "timerGrid", "Timer")
        self.stackSwitcher = Gtk.StackSwitcher()
        self.stackSwitcher.set_stack(self.stack)
        self.stackSwitcher.set_orientation(Gtk.Orientation.VERTICAL)

        #mainGrid
        self.mainGrid = Gtk.Grid()
        self.mainGrid.set_row_spacing(5)
        self.mainGrid.set_column_spacing(5)
        self.mainGrid.attach(self.stackSwitcher, 0,0,1,1)
        self.mainGrid.attach(self.stack, 1,0,1,1)
        self.add(self.mainGrid)

        self.layoutButton = Gtk.Button()
        self.layoutButton.set_label("Layout")
        self.layoutButton.connect("clicked",self.changeLayout)

        self.headerBarBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.headerBarBox.add(self.layoutButton)

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.pack_start(self.headerBarBox)
        self.headerBar.set_show_close_button(True)
        self.set_titlebar(self.headerBar)

    def on_button1_clicked(self, widget):
        self.button1.set_sensitive(False)
        self.button2.set_sensitive(True)
        self.t=threading.Thread(target=self.timing,args=())
        self.t.start()

    def on_button2_clicked(self, widget):
        self.button1.set_sensitive(True)
        self.button2.set_sensitive(False)
        self.t.run=False

    def timing(self):
        t = threading.currentThread()
        res=0.1
        time = 0
        while getattr(t, "run",True):
            time=time+res
            time=round(time*1000)/1000
            self.stopwatch_label.set_text(str(time)+"s")
            sleep(res)

    def timer(self):
        t = threading.currentThread()
        try:
            time=int(self.timer_entry.get_text())
        except:
            time=1
        while getattr(t, "run",True) and time>=0:
            self.timer_remaining_time_label.set_label(str(time)+"s")
            time=time-1
            sleep(1)
        for i in range(3):
            playsound("sounds/beep.mp3")
        self.timer_button.set_sensitive(True)
        self.timer_stop_button.set_sensitive(False)


    def start_timer(self,widget):
        self.t2 = threading.Thread(target=self.timer)
        self.t2.start()
        self.timer_button.set_sensitive(False)
        self.timer_stop_button.set_sensitive(True)

    def stop_timer(self,widget):
        self.t2.run = False

    def clock(self):
        t=threading.currentThread()
        while getattr(t,"run",True):
            self.clock_label.set_label(str(ctime(time())))
            sleep(1)

    def stop_all(self,widget):
        try:
            self.t1.run=False
        except:
            print("t1 wasnt running")
        try:
            self.t2.run=False
        except:
            print("t2 wasnt running")

        self.t3.run=False

    def changeLayout(self,widget):
        self.close()
        global openClassic
        openClassic = True

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

if openClassic:
    system("python3 simple_stopwatch.py")
