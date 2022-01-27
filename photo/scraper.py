import json
import os
import random
import re

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from photo.models import Photo

random.seed()
LOCATION_LIMIT = int(os.environ.get('LOCATION_LIMIT')) if os.environ.get('LOCATION_LIMIT') else 10
PHOTO_LIMIT = int(os.environ.get('PHOTO_LIMIT')) if os.environ.get('PHOTO_LIMIT') else 2
RAPIDAPI_KEY = '26ddeec01bmshe9a6ee3510e0f82p15ff58jsnd73a07927eee'
RAPIDAPI_HOST = 'instagram47.p.rapidapi.com'
USER_ID = 9892920103

# Caption remove
reg = re.compile('\@\w+|\#\w+|\r\n|\n|\r')

class PhotoScraper():

    @staticmethod
    def deEmojify(text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+")
        return emoji_pattern.sub(r'',text)

    @staticmethod
    def get_photos():
        print('Getting data')
        url = "https://instagram47.p.rapidapi.com/user_tagged_posts"

        querystring = {"userid": "1718924098"}

        headers = {
            'x-rapidapi-host': "instagram47.p.rapidapi.com",
            'x-rapidapi-key': "26ddeec01bmshe9a6ee3510e0f82p15ff58jsnd73a07927eee"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

        return json.loads(response.text)['body']['items']

if __name__ == "__main__":
    scraper = PhotoScraper()
    scraper.get_photos()