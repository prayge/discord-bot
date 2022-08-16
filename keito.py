from PIL import ImageFont, ImageDraw, Image
import chardet
import aiohttp
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
import time
from PIL import Image, ImageFont, ImageDraw
import io
import string
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
# dwd


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

bot = commands.Bot(command_prefix=['its', 'Its', "It's"])

cursor = connection.cursor()


class PaginationListPhrases(menus.ListPageSource):
    def __init__(self, data, username):
        super().__init__(data, per_page=10)
        self.username = username

    async def format_page(self, menu, phrases):

        embed = discord.Embed(title=f"{self.username}'s Phrases",
                              description=f"{self.username}")
        offset = menu.current_page * self.per_page
        lines = '\n'.join(f'ID: {elem[2]}, {elem[0]}' for _,
                          elem in enumerate(phrases, start=offset))
        embed.add_field(
            name=f"Phrases", value=lines)
        return embed


def add_space(text, offset):
    for _ in range(len(text), offset):
        text = text + " "
    return text


class PaginationCardCollection(menus.ListPageSource):
    def __init__(self, data, username):
        super().__init__(data, per_page=10)
        self.username = username

    async def format_page(self, menu, phrases):

        embed = discord.Embed(
            title=f"{self.username.author.name}'s Colleciton")
        offset = menu.current_page * self.per_page

        edition_space_count = 5
        phrase_space_count = 41
        card_space_count = 5

        ll = []

        for _, elem in enumerate(phrases, start=offset):
            edition = str(elem[0])
            phrase = str(elem[1])
            card = str(elem[2])

            e = add_space(edition, edition_space_count)
            p = add_space(phrase, phrase_space_count)
            c = add_space(card, card_space_count)

            ll.append(
                f'**Edition:** `{e}` **Phrase:** `{p}` **Card:** `{c}`')

        text = "\n".join(ll)

        embed.add_field(
            name=f"Cards", value=text)
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


class GiveConfirm(menus.Menu):
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


class DropConfirm(menus.Menu):
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
        self.result = 1
        self.stop()

    @ menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = 0
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


@ bot.command(name="links")
async def links(ctx, message: str):

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
@ commands.cooldown(1, 1, commands.BucketType.user)
async def drop(ctx):

    no_link_df = pd.read_sql(
        "select phrase from phrases where username = 'Keito' ", connection)
    no_links = no_link_df[~no_link_df['phrase'].str.contains("http")]
    phrases = no_links.to_dict('list')["phrase"]

    # randoms
    photo = random.choice(os.listdir("lib/pics"))
    frame = random.choice(os.listdir("lib/frames"))
    phrase = random.choice(phrases)
    old_phrase = phrase
    id = 1  # temp
    potential_owner = ctx.author.id
    print(id, photo, phrase, frame, potential_owner)

    drops = pd.read_sql(
        "select * from drops ", connection)
    drop = drops.to_dict('records')
    print(drops)

    letters_and_digits = string.ascii_letters + string.digits
    cardid = ''.join((random.choice(letters_and_digits)
                      for i in range(5))).upper()
    print(cardid)

    for elem in drop:
        if elem["id"] == id and elem["photo"] == photo and elem["phrase"] == phrase:
            id += 1

    print(id, photo, phrase, frame, potential_owner)

    if len(phrase) > 22:
        spaces = [i for i, char in enumerate(
            phrase) if char in string.whitespace]
        print(spaces)
        index = int(len(spaces)/2)
        print(index)

        phrase = phrase[:spaces[index]] + "\n" + phrase[spaces[index] + 1:]

    print("opening")
    im = Image.open("lib/pics/" + photo)
    im2 = Image.open("lib/frames/" + frame)

    print("drawing")
    im.paste(im2, (0, 0), im2)
    font_fam = "lib/fonts/impact.ttf"
    font = ImageFont.truetype(font_fam, 45)  # load font
    cardid_font = ImageFont.truetype(font_fam, 25)  # load font

    draw = ImageDraw.Draw(im)

    w, h = im.size

    # edition and cardid
    print("adding text")
    draw.text((420, 850), f"{id}", (255, 255, 255), font=font)
    draw.text((140, 10), cardid, (255, 255, 255), font=cardid_font)

    if "\n" in phrase:
        draw.multiline_text((w/2, 720), f"{phrase}",
                            (0, 0, 0), font=font, align='center', anchor="ma")
    else:
        draw.multiline_text((w/2, 750), f"{phrase}",
                            (0, 0, 0), font=font, align='center', anchor="ma")
    print("saving")

    im.save(f"{cardid}.png")
    image_message = await ctx.send(file=discord.File(f'{cardid}.png'))
    url = image_message.attachments[0].url
    if os.path.exists(f"{cardid}.png"):
        os.remove(f"{cardid}.png")

    confirm = await DropConfirm(f'Do you want to add this special keito to your collection?').prompt(ctx)
    print(confirm)
    if confirm == 1:
        cursor.execute("""
            INSERT INTO drops(id, photo, phrase, frame, owner, cardid, url) VALUES(%s, %s, %s, %s, %s, %s, %s)
            """, (id, photo, old_phrase, frame, potential_owner, cardid, url))
        connection.commit()
        await ctx.send(f"{ctx.author.mention}, Saved this keito to your collection!")
        print(f"saved to database with owner {potential_owner}")
    if confirm == 0 or confirm is None:
        cursor.execute("""
            INSERT INTO drops(id, photo, phrase, frame, cardid, url) VALUES(%s, %s, %s, %s, %s, %s)
            """, (id, photo, old_phrase, frame, cardid, url))
        connection.commit()
        print(f"saved to database with no owner")


@ bot.command(name="collection", aliases=['c'])
async def collection(ctx):
    drops = pd.read_sql(
        "select * from drops ", connection)
    drop = drops.to_dict('records')

    owner = ctx.author.id
    user_cards = []
    for d in drop:
        if d["owner"] is not None:
            if int(d["owner"]) == int(owner):
                user_cards.append([d["id"], d["phrase"], d["cardid"]])

    pages = MyMenuPages(source=PaginationCardCollection(
        user_cards, ctx), clear_reactions_after=True)
    await pages.start(ctx)

    # refactor sql to only select card information where username = me


@ collection.error
async def collection_message_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"{ctx.author.mention}, You have no cards in your collection, please collect cards using 'itsdrop'")


@ bot.command(name="view", aliases=['v'])
async def view(ctx, message: str):

    card_dict = pd.read_sql(
        f"select * from drops where cardid = '{message}'", connection)
    cards = card_dict.to_dict('records')
    card = cards[0]

    edition = card["id"]
    photo = card["photo"]
    phrase = card["phrase"]
    frame = card["frame"]
    owner = card["owner"]
    cardid = card["cardid"]
    url = card["url"]

    em = discord.Embed(title="Card Details",
                       description=f"Owned by <@{owner}>")
    em.add_field(
        name="Card Details", value=f'\n\n**Edition:** `{edition}` \n**Phrase:** `{phrase}` \n**Card:** `{cardid}`')

    if url is not None:
        em.set_image(url=url)

    # em add url

    await ctx.channel.send(embed=em)


@ view.error
async def view_message_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention}, You forgot to add a card to view, please add a card ID.")


@ bot.command(name="give")
async def give(ctx, message: str):

    card_dict = pd.read_sql(
        f"select * from drops where cardid = '{message}'", connection)
    cards = card_dict.to_dict('records')
    card = cards[0]

    sender_id = int(ctx.author.id)
    content = ctx.message.content
    mention_id = int(ctx.message.mentions[0].id)
    card_owner_id = int(card["owner"])

    card_id = content[7:].replace(
        f'{mention_id}', '').replace("<@>", "").strip()

    print(card_id)
    print(sender_id)
    print(content)
    print(mention_id)
    print(card_owner_id)

    if card_owner_id == sender_id:
        card_dict = pd.read_sql(
            f"select * from drops where cardid = '{message}'", connection)
        cards = card_dict.to_dict('records')
        card = cards[0]

        edition = card["id"]
        phrase = card["phrase"]
        owner = card["owner"]
        cardid = card["cardid"]
        url = card["url"]

        em = discord.Embed(title="Card Details",
                           description=f"Owned by <@{owner}>")
        em.add_field(
            name="Card Details", value=f'\n\n**Edition:** `{edition}` \n**Phrase:** `{phrase}` \n**Card:** `{cardid}`')

        if url is not None:
            em.set_image(url=url)

        # em add url

        await ctx.channel.send(embed=em)
        confirm = await DropConfirm(f'<@{sender_id}>, Do you want to give this card to <@{mention_id}>').prompt(ctx)
        if confirm == 1:
            cursor.execute(
                f"UPDATE drops SET owner = '{mention_id}' where cardid = '{card_id}';", ())
            connection.commit()
            await ctx.send(f"{ctx.author.mention}, You have successfuly given card `{card_id}` to <@{mention_id}>")

        if confirm == 0:

            await ctx.send(f"{ctx.author.mention}, Card give not accepted for `{card_id}`")
    else:
        await ctx.channel.send("You dont own this card")
        print("i dont own it")


@ bot.command(name="use", aliases=['u'])
async def use(ctx):
    author = ctx.author.name
    await ctx.send(f"{author}, fuck off hes not ready")


@ bot.command(name="inventory", aliases=['inv'])
async def inventory(ctx):
    author = ctx.author.name
    await ctx.send(f"{author}, fuck off hes not ready")


@ drop.error
async def drop_cooldown_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        secs = time.strftime("%M minute and %S seconds",
                             time.gmtime(error.retry_after))
        await ctx.send(f"{ctx.author.mention}, Try again in {secs}")

bot.remove_command('help')


@ bot.command(name="help", aliases=['h'])
async def help(ctx):
    em = discord.Embed(title="Keito bot help",
                       description=f"Commands and how to use them")
    em.add_field(
        name="keito", value=f'Returns the user with a quote by keito or an image of the lovely boy  e.g. "itskeito"', inline=False)
    em.add_field(
        name="quote", value=f'Returns the user with a quote by user mentioned in the message, e.g. "itsquote Patryk"', inline=False)
    em.add_field(
        name="add", value=f'Adds a quote for a specified user e.g. "itsadd !p <THE QUOTE> !u <THE USER>"', inline=False)
    em.add_field(
        name="delete", value=f'deletes a quote for a specified ID e.g. "itsdelete !id <QUOTE ID>"', inline=False)
    em.add_field(
        name="list", value=f'Lists the quotes (NOT IMAGE LINKS) for a user e.g. "itslist <USERNAME>"', inline=False)
    em.add_field(
        name="links", value=f'Lists the IMAGE LINKS for a user e.g. "itslinks <USERNAME>"', inline=False)
    em.add_field(
        name="users", value=f'Lists all users with a quote e.g. "itsusers",', inline=False)
    em.add_field(
        name="images", value=f'Creates an embed with images of user e.g. "itsimages <USERNAME>"', inline=False)
    em.add_field(
        name="drop", value=f'Drops a keito e.g. "itsdrop"', inline=False)
    em.add_field(
        name="collection", value=f'Displays all cards associated with user e.g. "itscollection"', inline=False)
    em.add_field(
        name="view", value=f'Displays card and information with associated card in message e.g. "itsview <CARD ID>"', inline=False)
    em.add_field(
        name="give", value=f'Give a card to a user e.g. "itsgive <CARD ID> <USER @, use the @ please>. Example "itsgive GF2FS @mordingo"', inline=False)

    await ctx.channel.send(embed=em)


@ quote.error
@ add.error
@ delete.error
@ list.error
@ users.error
async def send_error(ctx, error):
    print(type(error))
    await ctx.send(error)

bot.run(TOKEN)
