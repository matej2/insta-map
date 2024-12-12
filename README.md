# Instagram Photo Map

An interactive map showcasing the locations where Instagram photos were taken. Built with OpenStreetMap and Django.

## Overview

Initially, this project utilized the public Instagram GraphQL API to extract photo URLs, descriptions, location names, and authors' names. This data was directly displayed in map pop-ups, with hashtags and mentions removed from descriptions for cleaner display.

However, Instagram later introduced a time-based token for image URLs, rendering them valid for only about 48 hours. To address this, the project switched to using embedded posts, leveraging the available post IDs for a more stable solution.

## Status

**Note:** This project is currently deprecated due to Instagram's transition to a private API.


# Instructions

1. `pipenv run python manage.py migrate`
2. `pipenv run pyton manage.py runserver`
3. `pipenv run python insta_map/manual.py`
