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
cursor = connection.cursor()


only_ethan = pd.read_sql(
    "select * from lines where username = 'Ethan'", connection)
print(only_ethan)

# insert = "INSERT INTO lines(id, phrase, username) VALUES (42, 'test', 'loser')"
# cursor.execute(insert)


# table = pd.read_sql('select * from lines', connection)
# print(table)

# delete = "DELETE FROM lines WHERE id = '42'"
# cursor.execute(delete)

# table = pd.read_sql('select * from lines', connection)
# print(table)
