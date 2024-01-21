import socket
from Encryption import *
import threading
# from KivyClasses import MyApp
from MouseControl import *


class Server:
    def __init__(self):
        print("making a server")
        self.ip = get_ip()
        self.ip_encrypted = encrypt(self.ip)  # use encryption
        self.display_code = space_string(self.ip_encrypted)
        self.port = get_port()
        self.server_thread = None
        self.server_stop_event = threading.Event()
        self.hosting_event = threading.Event()
        # self.our_mouse = Mouse(1)

    def host(self):
        if self.is_hosting():
            return
        print("setting up server")
        self.server_stop_event.clear()
        self.server_thread = threading.Thread(target=self.private_host).start()  # pribably dont need to save as a variable

    def is_hosting(self):
        return self.hosting_event.is_set()

    def close_connection(self):
        if self.is_hosting():
            print("closing server")
            self.server_stop_event.set()
            self.hosting_event.clear()

    def private_host(self):
        """
        setup server
        :return:
        """
        self.hosting_event.set()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", self.port + 2))

            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    print(data)
                    interpret_text(data)
                    if not data or self.server_stop_event.is_set():
                        
                        s.shutdown()
                        break
                    conn.sendall(data)


class Client:
    def __init__(self):
        self.sock = None
        print("making client")
        self.port = get_port()
        self.connected = False

    def connect(self, target_device, is_encrypted = False):
        """
        if the target device is encrypted, decrypt it then connect
        :param target_device:
        :param is_encrypted: is the target_device encrypted?
        :return:
        """
        if is_encrypted:
            return self.connect_logic(decrypt(target_device))
        else:
            return self.connect_logic(target_device)

    def connect_logic(self, target_ip):
        """
        actually connect to the target ip
        :param target_ip:
        :return:
        """
        try:
            target_ip = "" # "172.16.13.27"
            print("trying to get connection to", target_ip)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("socket created")
            self.sock.connect((target_ip, self.port))
            print("socket connected")
            self.sock.sendall(b"Hello, world")
            self.connected = True
            print("sample message sent")
            return True
        except:
            return False

    def send(self, message):
        print("sending")
        if not self.connected:
            return
        self.sock.sendall(message.encode('utf-8'))

    def send_vector(self, x, y):
        if not self.connected:
            return
        msg = f"({x},{y})"
        print(f"sending {msg}")
        self.sock.sendall(msg.encode('utf-8'))

    def close(self):
        if not self.connected:
            return
        self.connected = False
        self.sock.close()


def get_ip():
    """gets this devices IP and, for now, prints it"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()
    # print(ip)
    # print(ip[0])
    s.close()
    return ip[0]


def get_port():
    """gets the port to use"""
    return 8089  # replace with actual algorithm at some point
