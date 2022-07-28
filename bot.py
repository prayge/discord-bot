import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
urls = []

with open("bingus", "rb") as fp:   # Unpickling
    urls = pickle.load(fp)


@client.event
async def on_ready():
    print("bingusbot Online")


@client.event
async def on_message(message):
    if message.content.startswith('bingus'):
        channel = message.channel
        await channel.send(random.choice(urls))


client.run(TOKEN)
