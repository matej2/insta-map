Interactive map that shows where Instagram photos were taken. Made in Open map and Django.

In first version I use public Instagram GraphQL API. I extract photo urls, description, location name and authors name. I can use this data directly to display them in map popup. I also remove any hashtags and mentions from description.

Instagram later implemented a time-based token for its images, which meant that image URLs were valid only for about 48 hours. I came to the conclusion that the most simple solution is to use embedded functionality, since I already have post IDs available.

**Project is currentl depreciated due to Instagram setting its API to private**

# Instructions

1. `pipenv run python manage.py migrate`
2. `pipenv run pyton manage.py runserver`
3. `pipenv run python insta_map/manual.py`
