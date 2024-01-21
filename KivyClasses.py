'''from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput'''
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.app import App
# from functools import partial
# from Touching import *
from kivy.lang import Builder
from kivy.core.window import Window
import math

import Matchmaking
from MouseControl import *
from Matchmaking import Client, Server
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


class InteractableImage(Image):
    new_size = Window.size
    movement_mode = 1  # 1 = absolute, -1 = relative
    # if absolute, just use total pos, and reposition the smaller widget
    # if relative, use dpos rather than pos, and uses relative movement
    # I don't have to convert this to a vector to use it.

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
        if self.movement_mode == 1:
            # print(touch.pos)
            self.check_vector(touch.pos[0], touch.pos[1])
        self.check_window_size()

    def check_vector(self, x, y):
        x = self.center[0] - x
        y = self.center[1] - y
        magnitude = math.sqrt(x*x + y*y)
        if magnitude < self.radius * 0.75:
            print("valid movement,", x, y)
            # main_mouse.move_mouse(x, y)
            client.send_vector(x, y)
            # convert to vector and send to brain

    def check_window_size(self):
        if self.default_window_size != Window.size:
            # print("we got an issue")
            self.set_sizes()
        else:
            pass

    def toggle_movement_mode(self):
        self.movement_mode *= -1


class ToggleableButton(Button):
    state = False
    true_text = ""
    false_text = ""
    def __init__(self, *args, **kwargs):
        super(InteractableImage, self).__init__(*args, **kwargs)

    def setup(self, true_text, false_text):
        self.true_text = true_text
        self.false_text = false_text

    def toggle(self):
        self.state = not self.state
        if self.state:
            self.text = self.true_text
        else:
            self.text = self.false_text
    

class MyApp(App):  # see if you can add touch widget to kv file?
    # new_pos = Window.size
    # new_size = Window.size
    send_sentence = False
    connected = False

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        # self.mouse = main_mouse
        self.file = Builder.load_file("kivy files/display.kv")

        # self.online_object = OnlineObject()

    def build(self):
        print()
        # initialise toggleable button values
        return self.file

    def on_close(self):
        server.close_connection()

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

    def checkbox_click(self):
        self.send_sentence = not self.send_sentence

    def toggle_connect(self):
        btn = self.root.ids.toggle_connection_btn
        if not client.connected:
            target_ip = self.root.ids.input.text
            three_numbers = "\d{0,3}"
            ip_format = f"^{three_numbers}[.]{three_numbers}[.]{three_numbers}[.]{three_numbers}"
            if bool(regex.match(ip_format, target_ip)) or target_ip == "":  # target_ip == "" means use local host
                if client.connect(target_ip):
                    btn.text = "connected"
                else:
                    btn.text = "couldnt find device with target ip"
            else:
                btn.text = "invalid ip format"
        else:
            client.close()

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
        if not self.send_sentence:
            self.on_enter_pressed()

    def on_enter_pressed(self):
        text = self.root.ids.input.text
        if text == "" or not client.connected:
            return
        self.root.ids.input.text = ""
        client.send("/" + text + "/")
        print("sending data to computer")

    code = "12345"

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