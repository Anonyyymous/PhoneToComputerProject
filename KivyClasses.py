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
from Math import *
from Matchmaking import Client, Server, get_name_ip_list, write_name_ip_lists
import regex


connected = False
host = False
sensitivity = 1
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
    movement_mode = -1
    # 1 = relative, so relative to last mouse position
    # -1 = absolute, so from center of the widget

    def __init__(self, *args, **kwargs):
        super(InteractableImage, self).__init__(*args, **kwargs)
        self.default_window_size = Window.size
        self.radius = 0
        self.height = 0
        self.width = 0
        self.set_sizes()
        # setup instance of image that we can grab and un-grab on touch down and up respectively
        btn = Button(text='te')
        self.add_widget(btn)

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
        if self.movement_mode == 1:
            self.check_vector(touch.dpos[0], touch.dpos[1])
        else:
            self.check_vector((touch.pos[0] - self.center_x) * sensitivity/10, 
                              (touch.pos[1] - self.center_y) * sensitivity/10)
        self.check_window_size()

    def check_vector(self, x, y):
        magnitude = math.sqrt(x*x + y*y)
        if magnitude < self.radius * 0.75:
            print("valid movement,", x, y)
            # main_mouse.move_mouse(x, y)
            client.send_vector(x * sensitivity, y * sensitivity)
            # convert to vector and send to brain

    def check_window_size(self):
        if self.default_window_size != Window.size:
            # print("we got an issue")
            self.set_sizes()
        else:
            pass

    def toggle_movement_mode(self):
        self.movement_mode *= -1


class MyApp(App):  # see if you can add touch widget to kv file?
    # new_pos = Window.size
    # new_size = Window.size
    send_sentence = False
    connected = False
    capslock = False
    ips_dict = {}
    saved_device_name = ""
    stored_ip = ""
    names = []
    ips = []
    temp_bool = False
    min_sens = 0.5
    max_sens = 5

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        # self.mouse = main_mouse
        self.file = Builder.load_file("kivy files/display.kv")
        self.names, self.ips = get_name_ip_list()
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
        # self.names, self.ips = get_name_ip_list()
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
            if client.connect(self.stored_ip):
                btn.text = 'connected'
            else:
                btn.text = 'couldnt find target ip'
        else:
            client.close()

    def set_spinner_options(self, spinner, list):
        spinner.values = list
        self.temp_bool = True
        spinner.text = list[0]
        self.temp_bool = False

    def create_ip_dropdown_buttons(self, is_different = False):
        if len(self.names) == 0 or len(self.ips) == 0:
            return
        self.set_spinner_options(self.root.ids.phone_ip_spinner, self.names)
        self.set_spinner_options(self.root.ids.pc_ip_spinner, self.names)
        self.stored_ip = self.ips[0]

        if is_different:
            write_name_ip_lists(self.names, self.ips)

    def check_ip_format(self, ip):
        three_numbers = "\d{0,3}"
        ip_format = f"^{three_numbers}[.]{three_numbers}[.]{three_numbers}[.]{three_numbers}"
        if bool(regex.match(ip_format, ip)):
            return True
        else:
            self.root.ids.pc_ip_add_ip.text += "\ninvalid ip format"
            return False
        
    def make_new_ip(self):
        print("making new ip")
        name = self.root.ids.pc_ip_add_name.text
        ip = self.root.ids.pc_ip_add_ip.text

        # if name in self.names:
            # return
        if not self.check_ip_format(ip):
            return

        self.names.append(name)
        self.ips.append(ip)

        self.create_ip_dropdown_buttons(True)

    def delete_name_ip(self, device_name):
        print("deleting line", device_name)
        if device_name in self.names:
            index = self.names.index(device_name)
            ip = self.ips[index]
            self.names.remove(device_name)
            self.ips.remove(ip)

    def select_target_ip(self, new_target_device_name):  # could just do this in the lambda function
        if self.temp_bool:
            return
        if not host:  # if on phone mode
            if new_target_device_name in self.names:
                index = self.names.index(new_target_device_name)
                self.stored_ip = self.ips[index]
                print("current ip =", self.stored_ip)
        else:
            print("select target ip")
            self.delete_name_ip(new_target_device_name)
            self.create_ip_dropdown_buttons(True)

    def quit(self):
        self.on_close()
        self.root_window.close()

    def mouse_sensitivity_changed(self, slider):
        # print(slider.value)
        global sensitivity
        sensitivity = lerp(self.min_sens, self.max_sens, slider.value)
        
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