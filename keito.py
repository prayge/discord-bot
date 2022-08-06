from __future__ import nested_scopes
from ast import alias
from discord.ext import commands, menus
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


class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        return f"This is number {entries}."


@bot.command()
async def test(ctx):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    formatter = MySource(data, per_page=1)
    menu = menus.MenuPages(formatter)
    await menu.start(ctx)


@bot.event
async def on_ready():
    timelapse = time.time()
    print(f"keitobot Online - took {timelapse-start} seconds")


@bot.command(name="quote", alias='q')
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


@bot.command(name="add", alias='a')
async def add(ctx, *, message: str):
    try:
        phrase_index = message.index("!p")
        user_index = message.index("!u")
        print(phrase_index, user_index)

        phrase = message[phrase_index+2:user_index].strip()
        user = message[user_index+2:len(message)].strip()
        # cursor.execute(
        #     f"INSERT INTO phrases(phrase, username) VALUES('{phrase}', '{user}')")

        # add button to accept add
        await ctx.send(f"Added phrase: {phrase} and username: {user} to database")
        connection.commit()
        print(f"added to db phrase: {phrase} and user: {user} ")
    except:
        await ctx.send("Add command formated incorrectly. please use '$add !p <phrase> !u <username> ")


@bot.command(name="delete", alias='d')
async def delete(ctx, *, message: str):
    try:
        id_index = message.index("!id")
        id = int(message[id_index+3:].strip())
        print(id)

        ids_df = pd.read_sql(
            "select id, phrase from phrases", connection)
        phrase_select = pd.read_sql(
            f"select phrase from phrases where id = {id}", connection)
        phrase_string = phrase_select.to_dict('list')
        phrase = "".join(phrase_string["phrase"])
        id_list = ids_df.to_dict('list')
        ids = id_list["id"]
        sorted_ids = sorted(ids, key=int)
        if sorted_ids.__contains__(id):
            print(f"{id} is in database")
            await ctx.send(f"Deleted {id}, which has phrase: {phrase} in database")
            # cursor.execute(
            # f"DELETE FROM phrases where id = {id}")

            # add button to accept delete
        else:
            await ctx.send(f"{id} doesnt exist in database, try again.")
            print(f"{id} not in database")

        connection.commit()
    except:
        await ctx.send("Add command formated incorrectly. please use '$delete !id <INTEGER> ")


@bot.command(name="list", alias='tl')
async def list(ctx, message: str):

    users = pd.read_sql(
        "select distinct username from phrases", connection)
    list_df = users.to_dict('list')
    list_usernames = list_df["username"]
    buttons = [u"\u25C0", u"\u25B6"]
    if message.strip() in list_usernames:
        try:
            list_df = pd.read_sql(
                f"select * from phrases where username = '{message}'", connection)
            listlist = list_df.values.tolist()
            ll = []
            for elem in listlist:
                if "https" not in elem[0]:
                    ll.append(elem)
                else:
                    print("http found")

            table = (
                "\n".join(f"ID: {elem[2]} Phrase: {elem[0]}" for elem in ll))

            embed = discord.Embed(title="Phrases",
                                  description=f"All the phrases said by {message}")
            embed.add_field(
                name=f"Phrases", value=table)
            msg = await ctx.send(embed=embed)
            for button in buttons:
                await msg.add_reaction(button)

        except:
            await ctx.send("Username doesnt exist, did you type it correctly? check current list of users with '$users' ")
    else:
        await ctx.send(f"Username {message} not in list of usernames")


@bot.command(name="users", alias='u')
async def users(ctx):
    users_df = pd.read_sql(
        "select distinct username from phrases", connection)
    list_df = users_df.to_dict('list')
    list_usernames = list_df["username"]
    usernames = ", \n".join(list_usernames)
    embed = discord.Embed(title="Users",
                          description=f"All the users in Database")
    embed.add_field(
        name=f"Users", value=usernames)
    await ctx.send(embed=embed)


@quote.error
@add.error
@delete.error
@list.error
async def send_error(ctx, error):
    print(type(error))
    await ctx.send(error)

bot.run(TOKEN)
