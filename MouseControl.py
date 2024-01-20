import mouse
import keyboard
import math
import regex
# from KivyClasses import host


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)


def vector_from_string(text):
    parts = text.split(",")
    x = float(parts[0][1:])
    y = float(parts[1][:-1])
    return Vector(x, y)


is_host = False
speed = 1
ticks_per_second = 1


def mouse_click(text):  # text should be [1], [2], or [3]
    text.lower()
    print(len(text))
    if len(text) != 3:
        print("mouse click input not valid")
        return
    elif text[1] == "1":
        mouse.click('left')
    elif text[1] == "2":
        mouse.click('right')
    elif text[1] == "3":
        mouse.click('middle')


def keyboard_input(text):
    print("keyboard input received")
    finding_key = False
    string_so_far = ""
    for char in text[1:-1]:
        if finding_key:
            if char == ">":
                finding_key = False
                keyboard.press(string_so_far.lower())
            string_so_far = string_so_far + char
        else:
            if char == "<":
                string_so_far = ""
                finding_key = True
            else:
                keyboard.press(char.lower())  # may need changing for maintaining case


def move_mouse(text):
    # if is_host:
    vector = vector_from_string(text)

    print("moving mouse, vector: ")
    print(vector.x, vector.y)
    vector *= (speed/ticks_per_second)
    mouse.move(vector.x, -vector.y, absolute=False)


def empty(text):
    print("empty input received;", text)


decimal_regex = "-?[0-9]+[.][0-9]+"
regex_formats = ["^/.+/", f"^[(]{decimal_regex},{decimal_regex}[)]", "^[[][0-9][]]", "^."]
functions = [keyboard_input, move_mouse, mouse_click, empty]
# keys to be input, mouse input, mouse position


def interpret_text(inp):
    text = inp.decode('utf-8')
    print("text received;", text)
    for i in range(len(regex_formats)):
        if bool(regex.search(regex_formats[i], text)):
            functions[i](text)
            break

