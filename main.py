from __future__ import unicode_literals
import discord
import discord.ext
import os
import random
import datetime
from discord.utils import get
import time
import logging 
import sys
import youtube_dl
import config

intents = discord.Intents.default()
intents.message_content = True
voice = discord.VoiceClient
channel = discord.channel

voicechannel = None

class MyLogger(object):
    def debug(self, msg):
        pass
    
    def warning(self,msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('finished download, converting...')


class MyClient(discord.Client):
    async def on_ready(self):
        print('We have logged in')

    async def on_error(self, event_method: str, /, *args: any, **kwargs: any) -> None:
        return await super().on_error(event_method, *args, **kwargs)

    async def on_message(self, message):
        voicechannel = None

        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        if message.content.startswith('$join'):
            where = message.content.split(" ")[1]
            url = message.content.split(" ")[2]
            channel = get(message.guild.channels, name=where)
            self.voicechannel = await channel.connect()

        if message.content.startswith('$play'):
            where = message.content.split(" ")[1]
            channel = get(message.guild.channels, name=where)
            self.voicechannel = await channel.connect()
            self.voicechannel.play(discord.FFmpegPCMAudio('Ark Survival Evolved 2022-11-26_2 - Copy.mp3'))
            #self.voicechannel.play(await discord.FFmpegOpusAudio.from_probe('Ark Survival Evolved 2022-11-26_2 - Copy.opus'))
            while self.voicechannel.is_playing():
                time.sleep(5)
            if self.voicechannel.is_paused():
                self.voicechannel.resume()

        if message.content.startswith('$pause'):
            if self.voicechannel.is_paused():
                await message.channel.send('The bot is already paused.')
            self.voicechannel.pause()

        if message.content.startswith('$resume'):
            if self.voicechannel.is_playing():
                await message.channel.send('The bot is already playing.')
            self.voicechannel.resume()

        if message.content.startswith('$leave'):
            print(dir(self.voicechannel))
            await self.voicechannel.disconnect()
            await discord.FFmpoegPCMAudio.cleanup

        if message.content.startswith('$exit'):
            sys.exit()

        if message.content.startswith('$help'):
            await message.channel.send('``` $help - zeigt alle Commands an\n $play [Channel] - spielt die datei im angegebenen Channel ab\n $pause - pausiert die wiedergabe\n $resume - setzt die wiedergabe fort\n $leave - Bot verlässt den Channel ```')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    }

discord.utils.setup_logging(level=logging.DEBUG)

client = MyClient(intents=intents)
client = client.run(config.token)