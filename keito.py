from sre_constants import NOT_LITERAL
from PIL import ImageFont, ImageDraw, Image
import datetime
import sys
from io import BytesIO
import requests
from discord.ext import commands, menus
from discord.ext.menus import button, First, Last
from discord.ext.commands import cooldown, BucketType

from dotenv import load_dotenv
import asyncio
import os
import random
import discord
import pickle
import psycopg2 as pg
import pandas as pd
import time
from PIL import Image, ImageFont, ImageDraw
import io


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

bot = commands.Bot(command_prefix='its')


cursor = connection.cursor()


class PaginationListPhrases(menus.ListPageSource):
    def __init__(self, data, username):
        super().__init__(data, per_page=10)
        self.username = username

    async def format_page(self, menu, phrases):

        embed = discord.Embed(title=f"{self.username}'s Phrases",
                              description=f"All the phrases said by this loser")
        offset = menu.current_page * self.per_page
        lines = '\n'.join(f'ID: {elem[2]}, {elem[0]}' for _,
                          elem in enumerate(phrases, start=offset))
        embed.add_field(
            name=f"Phrases", value=lines)
        return embed


class ImageListPagination(menus.GroupByPageSource):
    def __init__(self, entries):

        super().__init__(
            entries=entries,
            per_page=1,
            key=None,
            sort=False
        )

    async def format_page(self, menu, entry):
        print(entry)
        print(type(entry))

        entry_dict = entry[0]
        id = entry_dict["id"]
        phrase = entry_dict["phrase"]
        name = entry_dict["username"]

        embed = discord.Embed(title="Images")
        embed.add_field(
            name=f"{name}'s Photos, *hes so cute*", value=f"ID: {id}")
        offset = menu.current_page * self.per_page
        embed.set_image(url=phrase)
        return embed


class MyMenuPages(menus.MenuPages, inherit_buttons=False):
    @ button('\u2B05\uFE0F', position=First(1))
    async def go_to_previous_page(self, payload):
        await self.show_checked_page(self.current_page - 1)

    @ button('\u27A1\uFE0F', position=Last(1))
    async def go_to_next_page(self, payload):
        await self.show_checked_page(self.current_page + 1)


class Confirm(menus.Menu):
    def __init__(self, msg):
        super().__init__(timeout=30.0, delete_message_after=True)
        self.msg = msg
        self.result = None

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.msg)

    @ menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def do_confirm(self, payload):
        self.result = True
        self.stop()

    @ menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = False
        self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result


@ bot.event
async def on_ready():
    timelapse = time.time()
    print(f"keitobot Online - took {timelapse-start} seconds")


@ bot.command(name="keito", aliases=['k'])
async def keito(ctx):
    df_dict = pd.read_sql(
        f"select * from phrases where username = 'Keito'", connection)
    json_print = df_dict.to_dict(orient='records')
    randint = random.randint(0, len(json_print)-1)
    phrase = json_print[randint]
    await ctx.send(f"{phrase['phrase']}")


@ bot.command(name="quote")
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


# add commands
@ bot.command(name="imgadd", aliases=['ia'])
async def imgadd(ctx, *, message: str):

    phrase = message
    user = "Keiruta"

    cursor.execute("""
        INSERT INTO phrases(phrase, username) VALUES(%s, %s)
        """, (phrase, user))

    await ctx.send(f"Added phrase: {phrase} and username: {user} to database")
    connection.commit()
    print(f"added to db phrase: {phrase} and user: {user} ")


# add commands
@ bot.command(name="add", aliases=['a'])
async def add(ctx, *, message: str):
    try:
        phrase_index = message.index("!p")
        user_index = message.index("!u")

        phrase = message[phrase_index+2:user_index].strip()
        user = message[user_index+2:len(message)].strip()
        cursor.execute("""
            INSERT INTO phrases(phrase, username) VALUES(%s, %s)
            """, (phrase, user))

        await ctx.send(f"Added phrase: {phrase} and username: {user} to database")
        connection.commit()
        print(f"added to db phrase: {phrase} and user: {user} ")
    except:
        await ctx.send("Add command formated incorrectly. please use '$add !p <phrase> !u <username> ")


@ bot.command(name="delete")
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

        confirm = await Confirm(f'Delete phrase: {phrase}?').prompt(ctx)
        if confirm:
            if sorted_ids.__contains__(id):
                print(f"{id} is in database")
                await ctx.send(f"Deleted {id}, which has phrase: {phrase} in database")
                cursor.execute(
                    f"DELETE FROM phrases where id = {id}")
                print(f"deleted  {phrase} @ id {id}")
            else:
                await ctx.send(f"{id} doesnt exist in database, try again.")
                print(f"{id} not in database")

        connection.commit()
    except:
        await ctx.send("Add command formated incorrectly. please use '$delete !id <INTEGER> ")


@ bot.command(name="list")
async def list(ctx, message: str):

    users = pd.read_sql(
        "select distinct username from phrases", connection)
    list_df = users.to_dict('list')
    list_usernames = list_df["username"]
    if message.strip() in list_usernames:
        try:
            list_df = pd.read_sql(
                f"select * from phrases where username = '{message}'", connection)
            listlist = list_df.values.tolist()
            no_links = []
            links = []
            for elem in listlist:
                if "https" not in elem[0]:
                    no_links.append(elem)
                else:
                    links.append(elem)

            pages = MyMenuPages(source=PaginationListPhrases(
                no_links, message), clear_reactions_after=True)
            await pages.start(ctx)

        except:
            await ctx.send("Username doesnt exist, did you type it correctly? check current list of users with '$users' ")
    else:
        await ctx.send(f"Username {message} not in list of usernames")


@ bot.command(name="listlinks")
async def listlinks(ctx, message: str):

    users = pd.read_sql(
        "select distinct username from phrases", connection)
    list_df = users.to_dict('list')
    list_usernames = list_df["username"]
    if message.strip() in list_usernames:
        try:
            list_df = pd.read_sql(
                f"select * from phrases where username = '{message}'", connection)
            listlist = list_df.values.tolist()
            no_links = []
            links = []
            for elem in listlist:
                if "https" not in elem[0]:
                    no_links.append(elem)
                else:
                    links.append(elem)

            pages = MyMenuPages(source=PaginationListPhrases(
                links, message), clear_reactions_after=True)
            await pages.start(ctx)

        except:
            await ctx.send("Username doesnt exist, did you type it correctly? check current list of users with '$users' ")
    else:
        await ctx.send(f"Username {message} not in list of usernames")


@ bot.command(name="users", alias=['u'])
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


@ bot.command(name="images", aliases=['i'])
async def images(ctx, message: str):

    users_df = pd.read_sql(
        f"SELECT phrase, id, username FROM phrases WHERE( phrase LIKE 'http%' AND username = '{message}')", connection)
    list_df = users_df.to_dict('records')

    image_embed = MyMenuPages(source=ImageListPagination(
        list_df), clear_reactions_after=True)
    await image_embed.start(ctx)


@ bot.command(name="draw")
async def draw(ctx, message: str):

    if "http" in message:
        try:
            print(message)
            url = message
            response = requests.get(url)

            with Image.open(BytesIO(response.content)) as im:

                fnt = ImageFont.truetype("impact.ttf", 75)
                # get a drawing context
                d = ImageDraw.Draw(im)
                w, h = im.size

                # draw multiline text
                d.text(xy=(w/2, 10), text="GIVE SAM ", font=fnt,
                       fill="white", stroke_fill="black", anchor="mt", stroke_width=2)

                d.text(xy=(w/2, h-10), text="HIS MONEY", font=fnt,
                       fill="white", stroke_fill="black", anchor="ms", stroke_width=2)
                print("saving")
                im.save("test.png")

                await ctx.send(file=discord.File('test.png'))
        except:
            ctx.send("Invalid image, please try again")
    else:
        ctx.send("Not an image")


@ bot.command(name="drop", aliases=['d'])
@ commands.cooldown(1, 2, commands.BucketType.user)
async def drop(ctx):

    no_link_df = pd.read_sql(
        "select phrase from phrases where username = 'Keito' ", connection)
    no_links = no_link_df[~no_link_df['phrase'].str.contains("http")]
    phrases = no_links.to_dict('list')["phrase"]

    drops = pd.read_sql(
        "select * from drops ", connection)
    drop = drops.to_dict('list')
    print(drops)

    # randoms
    pic = random.choice(os.listdir("pics"))
    frame = random.choice(os.listdir("frames"))
    phrase = random.choice(phrases)
    id = 1  # temp
    potential_owner = ctx.author.id

    print(id, pic, phrase, frame, potential_owner)

    im = Image.open("pics/" + pic)
    im2 = Image.open("frames/" + frame)

    # cursor.execute("""
    #     INSERT INTO drops(id, photo, phrase, frame, owner) VALUES(%s, %s, %s, %s, %s)
    #     """, (id, pic, phrase, frame, potential_owner))
    # connection.commit()

    # im.paste(im2, (0, 0), im2)
    # print("saving")
    # im.save("test.png")
    # await ctx.send(file=discord.File('test.png'))

# @drop.error
# async def command_name_error(ctx, error):
#     if isinstance(error, commands.CommandOnCooldown):
#         secs = time.strftime("%M minute and %S seconds",
#                              time.gmtime(error.retry_after))
#         await ctx.send(f"{ctx.author.mention}, Try again in {secs}")


@ quote.error
@ add.error
@ delete.error
@ list.error
@ users.error
async def send_error(ctx, error):
    print(type(error))
    await ctx.send(error)

bot.run(TOKEN)
