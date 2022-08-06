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
#         "CREATE TABLE phrases (id INT PRIMARY KEY, phrase varchar, username varchar);")
# except:
#     print("I can't drop our test database!")

# connection.commit()

# f = open(r'./phrases.csv', 'r')
# cursor.copy_from(f, 'phrases', sep=',')
# f.close()

# only_ethan = pd.read_sql(
#     "select * from phrases ", connection)
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
#         "ALTER TABLE phrases ADD COLUMN id SERIAL PRIMARY KEY;")
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


ids_df = pd.read_sql(
    "select distinct id from phrases", connection)
id_list = ids_df.to_dict('list')
ids = id_list["id"]
sorted_ids = sorted(ids, key=int)

for x in sorted_ids:
    print(x)
