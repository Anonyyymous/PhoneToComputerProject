# from Encryption import *
from Matchmaking import *
# from MouseControl import *
from KivyClasses import MyApp
# import customtkinter
# import kivy

# data = input()
data = "1.53.254.74"  # "jjjk...hfahf123',"
ip = get_ip()
print(space_string(encrypt(ip)))

'''mouse = main_mouse
mouse.left_click()'''

'''interpret_text("hello world")
interpret_text("/*e")
interpret_text("/*e*/")
print("waiting")

input("-")'''

app = MyApp()
app.run()
app.on_close()

# make it so that we kill the server thread on kivy.close()

inp = ""
'''while inp == "":
    inp = input("")
    vector = Vector(int(input("enter x")), int(input("enter y")))
    mouse.move_mouse(vector)'''


