import pickle
from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv
import os

load_dotenv()
GCS_TOKEN = os.getenv('GCS_TOKEN')
GCS_ID = os.getenv('GCS_ID')

gis = GoogleImagesSearch(
    GCS_TOKEN, GCS_ID)

# define search params:
_search_params = {
    'q': 'bingus meme',
    'num': 100,
    'safe': 'off',
    'fileType': ['png', 'jpg', 'gif'],
}

# this will only search for images:
a = gis.search(search_params=_search_params)
res = gis.results()

bingus_urls = []

for link in res:
    bingus_urls.append(link.url)

with open("bins", "ab") as out:
    pickle.dump(bingus_urls, out)
