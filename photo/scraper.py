import os
import random
import re
import requests

from insta_map.proxy import get_json, proxy_generator
from location.models import Location
from photo.models import Photo

random.seed()
LOCATION_LIMIT = int(os.environ.get('LOCATION_LIMIT')) if os.environ.get('LOCATION_LIMIT') else 10
PHOTO_LIMIT = int(os.environ.get('PHOTO_LIMIT')) if os.environ.get('PHOTO_LIMIT') else 2

def scrape_photos():
    st = 0
    st2 = 0

    proxies = proxy_generator()

    # Caption remove
    reg = re.compile('\@\w+|\#\w+')
    # Caption block
    nature = re.compile('outdoor|nature|water|tree|sky|plant|cloud|grass')

    data = Location.objects.all()

    for d in data:
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
                    caption = pic['edge_media_to_caption']['edges'][0]['node']['text'][:254]
                    caption = reg.sub("", caption)


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
                if st > PHOTO_LIMIT:
                    break

            # How many locations to read?
            st2 = st2 + 1
            if st2 > LOCATION_LIMIT:
                break

def invalidate_photos():
    data = Photo.objects.all()

    for p in data:
        if p.url is not None:
            code = requests.get(p.url).status_code
        else:
            code = 200
        if code != 200 or p.url is None:
            print("Removing {}".format(p.id))
            p.delete()