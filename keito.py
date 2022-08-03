import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print("keitobot Online")


@bot.listen('on_message')
async def sus(message):
    check = random.randint(0, 20)
    if (check == 9 and "?" in message.content) and ("http" not in message.content) and ("keito" not in message.content):
        channel = message.channel
        await channel.send("Your mother")

    if ("keito" in message.content or "Keito" in message.content) and ("@ItsKeito" not in message.content) and (message.author != bot.user):
        # database things
        await channel.send("testing")


@bot.command()
async def add(ctx, *, message: str):

    await ctx.send(f"{message} Added to keitobot. P.S. keito is a cutie ")


bot.run(TOKEN)
