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
# try:
#     cursor.execute(
#         "CREATE TABLE drops (id INT, photo varchar, phrase varchar, frame varchar);")
# except:
#     print("I can't drop our test database!")

# connection.commit()

# only_ethan = pd.read_sql(
#     "select * from drops ", connection)
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

cursor = connection.cursor()
try:
    cursor.execute(
        "ALTER TABLE drops ADD COLUMN owner varchar;")
    print("added")
except:
    print("I can't drop !")
connection.commit()

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

pic = random.choice(os.listdir("pics"))
frame = random.choice(os.listdir("frames"))
im = Image.open("pics/" + pic)
im2 = Image.open("frames/" + frame)

drops = pd.read_sql(
    "select * from drops ", connection)
drop = drops.to_dict('list')
print(drops)
