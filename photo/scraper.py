import json
import os
import random
import re

import django
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from insta_map.proxy import get_json, proxy_generator
from location.models import Location
from location.scraper import LocationScraper
from photo.models import Photo

random.seed()
LOCATION_LIMIT = int(os.environ.get('LOCATION_LIMIT')) if os.environ.get('LOCATION_LIMIT') else 10
PHOTO_LIMIT = int(os.environ.get('PHOTO_LIMIT')) if os.environ.get('PHOTO_LIMIT') else 2
RAPIDAPI_KEY = 'b33a4e08e0mshf8388f588a4853dp116382jsn592e1278c602'
RAPIDAPI_HOST = 'instagram47.p.rapidapi.com'
USER_ID = 9892920103

# Caption remove
reg = re.compile('\@\w+|\#\w+|\r\n|\n|\r')

class PhotoScraper():
    @staticmethod
    def scrape_photos():
        st = 0
        st2 = 0

        proxies = proxy_generator()


        # Caption block
        nature = re.compile('outdoor|nature|water|tree|sky|plant|cloud|grass')

        data = Location.objects.all()

        for d in data:
            photo_cnt = len(d.photo_set.all())
            if photo_cnt < PHOTO_LIMIT:
                loc_pics_limit = PHOTO_LIMIT - photo_cnt
            else:
                continue
            pics = get_json(f'https://www.instagram.com/explore/locations/{d.id}/?__a=1', proxy=proxies)

            if pics is not False:
                pics_json = pics["graphql"]["location"]

                location = d.name
                lat = pics_json["lat"]
                lng = pics_json["lng"]

                # Update location parameters
                loc = Location.objects.get(id=d.id)
                loc.lat = lat
                loc.lng = lng
                loc.website = pics_json["website"]
                loc.save()

                for r in pics_json['edge_location_to_media']['edges']:
                    pic = r["node"]
                    caption = ""

                    # Scrape picture details
                    # TODO fix production bug: get request returns login page and not json
                    pic_url = f'https://www.instagram.com/p/{pic["shortcode"]}'
                    """
                    accessibility_caption = ""
    
                    pic_details = get_json(pic_url + '/?__a=1', proxy=proxies)
                    if pic_details is not False and pic_details["graphql"]["shortcode_media"].get("accessibility_caption", None) is not None:
                        details_json = pic_details["graphql"]["shortcode_media"]
                        accessibility_caption = details_json.get("accessibility_caption", "")[:254]
    
                    # Check Picture for blacklist
                    if accessibility_caption != "" and nature.match(accessibility_caption) is None:
                        continue
                    """
                    # Remove words from caption
                    if len(pic['edge_media_to_caption']['edges']) > 0:
                        caption = pic['edge_media_to_caption']['edges'][0]['node']['text'][:200]
                        caption = reg.sub("", caption)
                        caption = PhotoScraper.deEmojify(caption)


                    # Update or create Picture
                    try:
                        p = Photo.objects.get(id=pic["shortcode"])
                    except Photo.DoesNotExist:
                        p = Photo()
                        p.id = pic["shortcode"]
                    p.thumbnail = pic["thumbnail_src"][:499]
                    p.caption = caption
                    p.location_id = d.id
                    #p.accessibility_caption = accessibility_caption
                    p.url = pic_url[:254]
                    p.save()
                    print('Updating picture {}'.format(pic["shortcode"]))

                    # How many pictures for each location?
                    st = st + 1
                    if st >= loc_pics_limit:
                        break

                # How many locations to read?
                st2 = st2 + 1
                if st2 >= LOCATION_LIMIT:
                    break

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
    def invalidate_photos():
        data = Photo.objects.all()

        for p in data:
            if p.url is not None:
                code = requests.get(p.thumbnail).status_code
            else:
                code = 200
            if code != 200 or p.url is None:
                print("Removing {}".format(p.id))
                p.delete()

    @staticmethod
    def process_photos():
        PhotoScraper.invalidate_photos()
        photos = PhotoScraper.get_photos()

        for pic in photos:
            # Process location
            if 'location' in pic:
                LocationScraper.process_location(loc=pic['location'])
            else:
                print('No location')
                continue

            try:
                p = Photo.objects.get(id=pic['code'])
            except Photo.DoesNotExist:
                p = Photo()
                p.id = pic['code']

            p.thumbnail = pic['image_versions2']['candidates'][0]['url'][:499]
            caption = reg.sub("", pic['caption']['text'])
            caption = PhotoScraper.deEmojify(caption)
            p.caption = caption
            if 'location' in pic:
                p.location_id = pic['location']['pk']
            p.url = f'https://www.instagram.com/p/{pic["code"]}'
            # p.accessibility_caption = accessibility_caption
            try:
                p.save()
            except:
                continue
            print('Updating picture {}'.format(pic["code"]))

    @staticmethod
    def get_photos():
        print('Getting data')
        url = "https://instagram47.p.rapidapi.com/user_tagged_posts"

        querystring = {"userid": USER_ID}

        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return json.loads(response.text)['body']['items']

if __name__ == "__main__":
    scraper = PhotoScraper()
    scraper.process_photos()