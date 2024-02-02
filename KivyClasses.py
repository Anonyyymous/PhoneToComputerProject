'''from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput'''
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.vkeyboard import VKeyboard
from kivy.app import App
# from functools import partial
# from Touching import *
from kivy.lang import Builder
from kivy.core.window import Window
import math

import Matchmaking
from MouseControl import *
from Matchmaking import Client, Server, get_name_ip_list
import regex


connected = False
host = False
# online_object = OnlineObject()
client = Client()
server = Server()
# client.connect("172.16.0.232", True)


def toggle_widget(wid):
    hide = not wid.disabled
    if not hide:
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 1, 1, 1, False
    elif hide:
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


def force_widget(wid, state):
    # hide = not wid.disabled
    if state:
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 1, 1, 1, False
    else:
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


class ButtonInt(Button):
    num = 0
    def __init__(self, start_value, *args, **kwargs):
        super(ButtonInt, self).__init__(*args, **kwargs)
        self.num = start_value


class InteractableImage(Image):
    new_size = Window.size
    sensitivity = 1


    def __init__(self, *args, **kwargs):
        super(InteractableImage, self).__init__(*args, **kwargs)
        self.default_window_size = Window.size
        self.radius = 0
        self.height = 0
        self.width = 0
        self.set_sizes()
        # setup instance of image that we can grab and un-grab on touch down and up respectively

    def set_sizes(self):  # automatically adjust sizes
        self.default_window_size = Window.size
        self.height = Window.size[1]/2
        self.width = Window.size[0]/2
        self.radius = int(self.height/2)
        self.center = (self.width/2 + 5, self.height/2 + 5)
        if self.height > self.width:  # we're too tall
            self.radius = int(self.width/2)
        print(self.radius)

    def on_touch_move(self, touch):
        self.check_vector(touch.dpos[0], touch.dpos[1])
        self.check_window_size()

    def check_vector(self, x, y):
        magnitude = math.sqrt(x*x + y*y)
        if magnitude < self.radius * 0.75:
            print("valid movement,", x, y)
            # main_mouse.move_mouse(x, y)
            client.send_vector(x * self.sensitivity, y * self.sensitivity)
            # convert to vector and send to brain

    def check_window_size(self):
        if self.default_window_size != Window.size:
            # print("we got an issue")
            self.set_sizes()
        else:
            pass


class MyApp(App):  # see if you can add touch widget to kv file?
    # new_pos = Window.size
    # new_size = Window.size
    send_sentence = False
    connected = False
    capslock = False
    ips = {}
    saved_device_name = ""

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        # self.mouse = main_mouse
        self.file = Builder.load_file("kivy files/display.kv")

        # self.online_object = OnlineObject()

    def build(self):
        print()
        # initialise toggleable button values
        return self.file
    
    def on_start(self, **kwargs):
        self.create_ip_dropdown_buttons()

    def on_close(self):
        server.close_connection()

    def toggle_settings(self):
        print("toggling settings")

    def swap_mode(self):
        global host
        toggle_widget(self.root.ids.pc)
        toggle_widget(self.root.ids.phone)
        if self.root.ids.phone.disabled:  # if phone is disabled, so we're on the pc mode
            host = True
            print("on pc mode")
        else:
            host = False
            print("on mobile mode")

    def toggle_sentence_send(self):
        self.send_sentence = not self.send_sentence
        btn = self.root.ids.toggle_sentence_send_btn
        if self.send_sentence:
            btn.text = "toggle send sentence:\nSending when 'send' clicked"
        else:
            btn.text = "toggle send sentence:\nSending individual char"

    def toggle_connect(self):
        btn = self.root.ids.toggle_connection_btn
        # self.root.ids.ip_dropdown.open()
        if not client.connected:
            '''target_ip = self.root.ids.input.text
            three_numbers = "\d{0,3}"
            ip_format = f"^{three_numbers}[.]{three_numbers}[.]{three_numbers}[.]{three_numbers}"
            if bool(regex.match(ip_format, target_ip)) or target_ip == "":  # target_ip == "" means use local host
                if client.connect(target_ip):
                    btn.text = "connected"
                else:
                    btn.text = "couldnt find device with target ip"
            else:
                btn.text = "invalid ip format"'''
            if client.connect(self.ips[self.saved_device_name]):
                btn.text = 'connected'
            else:
                btn.text = 'couldnt find target ip'
        else:
            client.close()

    def create_ip_dropdown_buttons(self):
        names, ips = get_name_ip_list()
        if len(names) == 0 or len(ips) == 0:
            return
        count = 0
        parent = self.root.ids.ip_spinner
        parent.values = names
        parent.text = names[0]
        self.saved_device_name = names[0]
        while count < len(names) and count < len(ips):
            '''main_btn = ButtonInt(count, text=names[count], height=66, size_hint_y=None)
            main_btn.bind(on_press= lambda btn_self: self.select_target_ip(ips[btn_self.num]))
            parent.add_widget(main_btn)
            parent.values = names'''
            self.ips[names[count]] = ips[count]

            count += 1
        self.stored_ip = ips[0]
        # in settings
        '''parent = self.root.ids.settings_ip_dropdown
        count = 0
        while count < len(names) and count < len(ips):
            layout = BoxLayout(orientation='horizontal')
            main_btn = ButtonInt(count, text=names[count], height=66, size_hint_y=None)
            main_btn.bind(on_press= lambda btn_self: self.select_target_ip(ips[btn_self.num]))

            del_btn = ButtonInt(count, text='x', on_press= lambda btn_self: self.delete_name_ip(ips[btn_self.num]))  # could be optimised to store this in a single BoxLayout class thing, but cba
            
            layout.add_widget(main_btn)
            layout.add_widget(del_btn)
            count += 1'''

    def delete_name_ip(self, line_num):
        print("deleting line", line_num)

    def select_target_ip(self, new_target_device_name):  # could just do this in the lambda function
        print("set target ip to", new_target_device_name)
        self.saved_device_name = "" + new_target_device_name
        if len(self.ips) > 0:  # this is called on start for some reasno
            print(self.ips[self.saved_device_name])

    def quit(self):
        self.on_close()
        self.root_window.close()

    def on_mouse_1(self, value):
        print("mouse 1 pressed")
        client.send(f"[1{value}]")

    def on_mouse_2(self, value):
        print("mouse 2 pressed")
        client.send(f"[2{value}]")

    def on_text_changed(self):
        print("e (188)")
        if not self.send_sentence:
            self.on_enter_pressed()

    def on_enter_pressed(self):
        text = self.root.ids.input.text
        if text == "" or not client.connected:
            return
        self.root.ids.input.text = ""
        client.send("/" + text + "/")
        print("sending data to computer")

    def vkeyboard_pressed(self, *args):
        key = args[0][1]
        print(key, "pressed")
        if len(key) > 1:
            if key.lower() == "capslock":
                self.capslock = not self.capslock
            self.root.ids.input.text = parse_text_command(key, self.root.ids.input.text)
            return
        if self.capslock:
            key = key.upper()
        self.root.ids.input.text += key

    code = "12345"

    # def on_touch_down(self, touch):
        # self.root.ids.ip_dropdown.open()

    def toggle_activity(self):
        btn = self.root.ids.toggle_server_connection_btn
        
        if not server.is_hosting():
            server.host()
            print("starting to host")
            btn.text = "looking for client"
        else:
            self.disconnect()
            print("disconnecting")
            btn.text = "stopped hosting"

    def toggle_code(self):
        code = self.root.ids.code_display.text
        if code == "":
            self.root.ids.code_display.text = Matchmaking.get_ip()
        else:
            self.root.ids.code_display.text = ""

    def disconnect(self):
        print("disconnecting")
        if host:
            server.close_connection()
            self.root.ids.toggle_server_connection_btn.text = "stopped hosting"
        else:
            client.close()
        # online_object.hosting_thread.is_alive = False

        self.root.ids.connected_checkbox.active = False
        # online_object.searching = False