"""
Copyright Kyle Guss 2018

For use specifically with Chat App (Oates3)

Send text_box over socket 3514/3515
"""

import socket
import threading
from tkinter import *


def on_entry_click(event):
    """when entering entry box, remove example message, set Text box state to normal"""
    if entry_box.get() == 'Type your message, press Enter to send.':
        entry_box.delete(0, "end")
        entry_box.insert(0, '')
        text_box.configure(state="normal")


def on_exit_click(event):
    """when leaving entry box, add example message, set Text box state to disabled"""
    if entry_box.get() == '':
        entry_box.insert(0, 'Type your message, press Enter to send.')
        entry_box.config(fg = 'grey')
        text_box.configure(state="disabled")


def get_data():
    """set up receive socket, loop for receiving data, swap states of text_box when adding message"""
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # UDP socket
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # set option reusable
    recv_sock.bind((udp_ip, udp_port_receive))
    while True:
        data, addr = recv_sock.recvfrom(1024)
        print("received message:", data)
        data = str(data)
        text_box.configure(state="normal")
        text_box.insert(INSERT, 'Ghost: %s\n' % data[2:-5])
        text_box.configure(state="disabled")


def enter_pressed(event):
    """take text from Entry, insert to text box, send over send_sock, reset Entry box"""
    input_get = entry_box.get()
    print("sent message: ", input_get)
    text_box.insert(INSERT, 'Me: %s\n' % input_get)
    send_sock.sendto(input_get.encode(), (udp_ip, udp_port_send))
    input_user.set('')
    return "break"


# CREDENTIALS
udp_ip = "127.0.0.1"
udp_port_send = 3514
udp_port_receive = 3515

# Set up send socket
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # UDP socket
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # set option reusable

get_data_thread = threading.Thread(target=get_data)                 # thread for receiving data
get_data_thread.start()

# Tk GUI setup
window = Tk()
window.title("351Sockets")
text_box = Text(window)
text_box.pack()
input_user = StringVar()
entry_box = Entry(window, text=input_user)
entry_box.insert(0, 'Type your message, press Enter to send.')
entry_box.bind('<FocusIn>', on_entry_click)                       # bind events
entry_box.bind('<FocusOut>', on_exit_click)
entry_box.bind("<Return>", enter_pressed)
entry_box.pack(side=BOTTOM, fill=X)
frame = Frame(window)
frame.pack()
text_box.configure(state="disabled")                                # disable state prevents adding text

# Threads
window.mainloop()                                                   # run tkinter loop
get_data_thread.join()
