import random
import re

from insta_map.proxy import get_json, proxy_generator
from location.models import Location
from photo.models import Photo

random.seed()


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
                accessibility_caption = ""
                pic_url = f'https://www.instagram.com/p/{pic["shortcode"]}'

                pic_details = get_json(pic_url + '/?__a=1', proxy=proxies)
                if pic_details is not False:
                    details_json = pic_details["graphql"]["shortcode_media"]
                    accessibility_caption = details_json.get("accessibility_caption", "")

                # Check Picture for blacklist
                if accessibility_caption != "" and nature.match(accessibility_caption) is None:
                    continue

                # Remove words from caption
                if len(pic['edge_media_to_caption']['edges']) > 0:
                    caption = pic['edge_media_to_caption']['edges'][0]['node']['text'][:400]
                    caption = reg.sub("", caption)


                # Update or create Picture
                try:
                    p = Photo.objects.get(id=pic["id"])
                except Photo.DoesNotExist:
                    p = Photo()
                    p.id = pic["id"]
                p.thumbnail = pic["thumbnail_src"]
                p.caption = caption
                p.location = d
                p.accessibility_caption = accessibility_caption
                p.url = pic_url
                p.save()
                print('Updating picture {}'.format(pic["id"]))

                # How many pictures for each location?
                st = st + 1
                if st > 2:
                    break

            # How many locations to read?
            st2 = st2 + 1
            if st2 > 70:
                break
