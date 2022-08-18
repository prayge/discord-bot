from collections import Counter
import string
import random
from io import BytesIO
from PIL import Image
import requests
from hashlib import new
from xmlrpc.server import list_public_methods
import psycopg2 as pg
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()

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

# table name is lines [id, phrase, username]

##############################  CREATE TABLE #############################

# cursor = connection.cursor()

# cursor.execute(
#     """CREATE TABLE images
#     (id SERIAL PRIMARY KEY,
#     imagename varchar,
#     imagebytes varchar);""")


# connection.commit()

# only_ethan = pd.read_sql(
#     "select * from images ", connection)
# print(only_ethan)

# connection.commit()
# connection.close()


##############################  TEST DF #############################

# only_ethan = pd.read_sql(
#     "select * from phrases where username = 'Ethan'", connection)

# json_print = only_ethan.to_dict(orient='records')
# print(json_print[0])


##############################  INSERT #############################

# cursor.execute(
#         "INSERT INTO phrases(player_name) VALUES(%(name)s)", {"name": message})

##############################  DROP COLUMN #############################

# cursor = connection.cursor()
# try:
#     cursor.execute(
#         "ALTER TABLE drops ADD COLUMN url varchar;")
#     print("added")
# except:
#     print("I can't drop !")
# connection.commit()

# only_ethan = pd.read_sql(
#     "select * from phrases where username = 'Keito'", connection)
# list_df = only_ethan.to_dict('list')
# list_phrases = list_df["phrase"]
# new_l = []

# for i, p in enumerate(list_phrases):
#     if "https" not in p:
#         new_l.append(p)

# phrases_test = '\n'.join(new_l)
# print(phrases_test)

# no_link_df = pd.read_sql(
#     "select phrase from phrases where username = 'Keito' ", connection)
# no_links = no_link_df[~no_link_df['phrase'].str.contains("http")]
# phrases = no_links.to_dict('list')["phrase"]

# # randoms
# photo = random.choice(os.listdir("pics"))
# frame = random.choice(os.listdir("frames"))
# phrase = random.choice(phrases)
# id = 1  # temp
# potential_owner = 170983161650610178

# print(id, photo, phrase, frame, potential_owner)

# drops = pd.read_sql(
#     "select * from drops ", connection)
# drop = drops.to_dict('records')
# print(drops)

# for elem in drop:
#     if elem["id"] == id and elem["photo"] == photo and elem["phrase"] == phrase:
#         id += 1


# cursor = connection.cursor()
# try:
#     cursor.execute(
#         "TRUNCATE TABLE drops;")
# except:
#     print("deleted the table")

# connection.commit()


# print(id, photo, phrase, frame, potential_owner)


e = pd.read_sql(
    "select * from drops", connection)
l = e.to_dict('list')["cardid"]

print(e)
