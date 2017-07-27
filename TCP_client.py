import socket
import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog
from time import sleep
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

TCP_IP = sys.argv[1]
TCP_PORT = 55555
TCP_FILE_PORT = 55556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    msg = input()

    if msg == "SEND_FILE":
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()

        with open(path, "rb") as f:
            FILE = f.read()

        s.send(("!BOF@" + path_leaf(path) + "@" + str(len(FILE)) + "\n").encode("utf-8"))

        sleep(1)

        file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_socket.connect((TCP_IP, TCP_FILE_PORT))
        file_socket.send(FILE)
        file_socket.close()

        s.send("!EOF@\n".encode("utf-8"))

    elif msg.lower() == "!close":
        break

    elif msg.lower() == "!clear":
        os.system("clear")

    else:
        s.send((msg + "\n").encode("utf-8"))

s.close()