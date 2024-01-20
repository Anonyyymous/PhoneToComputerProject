from ExtraInfo import *


def encrypt(data_to_encrypt):  # direction = 1
    new_string = ""
    for character in data_to_encrypt:
        # print(character)
        new_string = new_string + shift(character, data_to_encrypt.index(character), direction=1)
    return new_string


def decrypt(data_to_decrypt):  # direction = -1
    new_string = ""
    for character in data_to_decrypt:
        # print(character)
        new_string = new_string + shift(character, data_to_decrypt.index(character), direction=-1)
    return new_string


def shift(character, index, direction=1):
    # print("index =", index, len(CIPHER)-1)
    amended_index = index % len(CIPHER)
    pos = CHARACTERS.index(character)
    # print(f"shifting {character} by {CIPHER[amended_index]}")
    for i in range(int(CIPHER[amended_index])):
        pos += direction
        pos = pos % len(CHARACTERS)
    return CHARACTERS[pos]


def space_string(data, spacing=4):
    # spacing = spacing+1
    last_point = 0
    new_string = ""
    for i in range(len(data)):
        if i % spacing == 0 and i > 1:
            new_string = new_string + data[last_point:i] + " "
            last_point = i
    new_string = new_string + data[last_point:len(data)]
    return new_string
