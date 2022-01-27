import asyncio
import os

import django
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from photo.scraper import PhotoScraper

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()

    scheduler.add_job(PhotoScraper.get_photos, trigger=IntervalTrigger(hours=12))

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass