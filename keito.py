from __future__ import nested_scopes
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import discord
import pickle
import psycopg2 as pg
import pandas as pd


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

try:
    connection = pg.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD)
    print("Connected to database")
except:
    print('Can not access database')

bot = commands.Bot(command_prefix='$')
cursor = connection.cursor()


def print_msg(channel, query):
    df_dict = pd.read_sql(
        f"select * from phrases where username = '{query}'", connection)

    json_print = df_dict.to_dict(orient='records')
    randint = random.randint(0, len(json_print)-1)
    phrase = json_print[randint]
    return phrase


@bot.event
async def on_ready():
    print("keitobot Online")


@bot.listen('on_message')
async def sus(message):
    print(f"message.author: {message.author}")
    print(f"message.content:  {message.content}")
    print(f"message.embeds:  {message.embeds}")
    print(f"message.author.bot: {message.author.bot}")
    print(f"message.is_system(): {message.is_system()}")

    check = random.randint(0, 20)
    channel = message.channel

    if message.author.bot == True or message.author == bot.user:

        print(bot.user)
        print(f"im a bot")
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    else:
        if (check == 9 and "?" in message.content) and ("http" not in message.content) and ("keito" not in message.content):
            await channel.send("Your mother")

        if ("keito" in message.content.lower()) and ("@ItsKeito" not in message.content):
            query = "Keito"
            phrase = print_msg(channel, query)
            print(phrase)
            await channel.send(f"{phrase['phrase']}")

        if ("ethan" in message.content.lower()) and ("@Mordingo" not in message.content):

            query = "Ethan"
            phrase = print_msg(channel, query)
            await channel.send(f"{phrase['phrase']}")

        if ("jongtee" in message.content.lower()) and ("@Jongtee" not in message.content):
            query = "Patryk"
            phrase = print_msg(channel, query)
            await channel.send(f"{phrase['phrase']}")

        if("collector" in message.content):
            await channel.send("https://cdn.discordapp.com/attachments/815190898052300821/909895376167907358/unknown.png")


@bot.command()
async def add(ctx, *, message: str):
    print(message)
    phrase_num = message.find("!p")
    user_num = message.find("!u")

    phrase = message[phrase_num+2:user_num].strip()
    user = message[user_num+2:len(message)].strip()
    cursor.execute(
        f"INSERT INTO phrases(phrase, username) VALUES('{phrase}', '{user}')")
    await ctx.send(f"Added phrase: {phrase} and username: {user} to database")
    connection.commit()
    print(f"added to db phrase: {phrase} and user: {user} ")


@bot.command()
async def list(ctx, *, message: str):
    try:
        only_ethan = pd.read_sql(
            f"select * from phrases where username = '{message}'", connection)
        list_df = only_ethan.to_dict('list')
        list_phrases = list_df["phrase"]
        new_l = []

        for i, p in enumerate(list_phrases):
            if "https" not in p:
                new_l.append(p)

        phrases_test = '\n'.join(new_l)
        embed = discord.Embed(title="Phrases",
                              description=f"All the phrases said by {message}")  # ,color=Hex code
        embed.add_field(
            name=f"Phrases", value=phrases_test)
        await ctx.send(embed=embed)

    except:
        print(message)
        await ctx.send("Username doesnt exist, did you type it correctly? Make sure the Name is spelled correctly and has a Capital Letter. ex. 'Keito' ")

bot.run(TOKEN)
