# Instagram Photo Map

An interactive web application that visualizes the geographic locations of Instagram photos on a map. Built using **Django** for the backend and **OpenStreetMap** for the interactive map interface.

---

## Overview

The project initially utilized Instagram's public GraphQL API to fetch photo metadata, including:
- Photo URLs
- Descriptions (with hashtags and mentions removed for cleaner presentation)
- Location names
- Author names

This data was dynamically displayed in map pop-ups, providing users with an engaging way to explore photo locations.

However, Instagram introduced a time-based token system for image URLs, limiting their validity to approximately 48 hours. To adapt, the project transitioned to using embedded posts, leveraging post IDs for a more stable and reliable solution.

---

## Current Status

⚠️ **Deprecated**: This project is no longer actively maintained due to Instagram's transition to a private API, which restricts access to the required data.

---

## Setup Instructions

1. Run database migrations:
```bash
pipenv run python manage.py migrate
```
2. Start the development server:
```bash
pipenv run python manage.py runserver
```
3. Execute the manual script to fetch and process data:
```bash
pipenv run python insta_map/manual.py
```

---

This project demonstrates the challenges of working with third-party APIs and the need for adaptability in response to platform changes. While no longer functional, it serves as a case study in API integration and geospatial data visualization.
