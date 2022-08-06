from __future__ import nested_scopes
from ast import alias
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
import random
import discord
import pickle
import psycopg2 as pg
import pandas as pd
import time

start = time.time()

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
    timelapse = time.time()
    print(f"Connected to database - took {timelapse-start} seconds")
except:
    print('Can not access database')

bot = commands.Bot(command_prefix='$')
cursor = connection.cursor()


@bot.event
async def on_ready():
    timelapse = time.time()
    print(f"keitobot Online - took {timelapse-start} seconds")


@bot.listen('on_message')
async def sus(message):

    check = random.randint(0, 20)
    channel = message.channel

    if (check == 9 and "?" in message.content) and ("http" not in message.content):
        await channel.send("Your mother")

    if("collector" in message.content):
        await channel.send("https://cdn.discordapp.com/attachments/815190898052300821/909895376167907358/unknown.png")


@bot.command(alias='q')
async def quote(ctx, *, message: str):
    query = message
    users = pd.read_sql(
        "select distinct username from phrases", connection)
    list_df = users.to_dict('list')
    list_usernames = list_df["username"]
    usernames = ", ".join(list_usernames)
    if query in list_usernames:
        print("Works for this username")
        df_dict = pd.read_sql(
            f"select * from phrases where username = '{query}'", connection)
        json_print = df_dict.to_dict(orient='records')
        randint = random.randint(0, len(json_print)-1)
        phrase = json_print[randint]
        await ctx.send(f"{phrase['phrase']}")
    else:
        await ctx.send(f"{query} is not in list of usernames. the current list is {usernames}")


@bot.command(alias='a')
async def add(ctx, *, message: str):
    try:
        phrase_index = message.index("!p")
        user_index = message.index("!u")
        print(phrase_index, user_index)

        phrase = message[phrase_index+2:user_index].strip()
        user = message[user_index+2:len(message)].strip()
        # cursor.execute(
        #     f"INSERT INTO phrases(phrase, username) VALUES('{phrase}', '{user}')")
        await ctx.send(f"Added phrase: {phrase} and username: {user} to database")
        connection.commit()
        print(f"added to db phrase: {phrase} and user: {user} ")
    except:
        await ctx.send("Add command formated incorrectly. please use '$add !p <phrase> !u <username> ")


@bot.command(alias='d')
async def delete(ctx, *, message: str):
    try:
        id_index = message.index("!id")
        id = message[id_index+3:].strip()
        print(id)

        ids_df = pd.read_sql(
            "select distinct id from phrases", connection)
        id_list = ids_df.to_dict('list')
        ids = id_list["id"]
        sorted_ids = sorted(ids, key=int)
        [print(x) for x in sorted_ids]

        if sorted_ids.__contains__(int(id)):
            print(f"{id} is in database")
            # cursor.execute(
            # f"DELETE FROM phrases where id = {id}")
            await ctx.send(f"Deleted {id} in database")
        else:
            await ctx.send(f"{id} doesnt exist in database, try again.")
            print(f"{id} not in database")

        connection.commit()
    except:
        await ctx.send("Add command formated incorrectly. please use '$delete !id <id> ")


@bot.command(alias='l')
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
                              description=f"All the phrases said by {message}")
        embed.add_field(
            name=f"Phrases", value=phrases_test)
        await ctx.send(embed=embed)

    except:
        print(message)
        await ctx.send("Username doesnt exist, did you type it correctly? Make sure the Name is spelled correctly and has a Capital Letter. ex. 'Keito' ")

bot.run(TOKEN)
