'''
    Re-check for some additional feature

'''


# Discord Pkg
import discord
from discord.ext import commands


import time
import os

# view stream
from view_stream import view
from view_stream import client_socket


bot = commands.Bot(command_prefix='!')
bot_token = "OTYwNDYzMzY4Nzg1ODg3MzEy.YkqzNw.RF_q9YqNofIRo8E4gVkWBRfEUug"

@bot.event
async def on_ready():
    report_channel = bot.get_channel(959449626149285988)
    await report_channel.send("Program's Online and Ready")
    time.sleep(2)




@bot.command()
async def start_stream(message, ip: str):
    await message.send('Joining the server now')
    time.sleep(2)
    view(ip)
    print('sample')
    time.sleep(2)
    client_socket.close()



@bot.command()
async def rest(message):
    await message.send("We're going offline now")
    time.sleep(2)
    exit()


@bot.event
async def on_message(message):
    # .content to get a specific chats from the user
    if message.content == "Opening server now":
        # arduino.write(b'a')
        report_channel = bot.get_channel(959449626149285988)
        await report_channel.send('Just give me the IP for the stream')
        time.sleep(2)
    await bot.process_commands(message)

bot.run(bot_token)
