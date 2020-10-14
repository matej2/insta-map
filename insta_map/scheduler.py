import asyncio
import os

import django
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from location.scraper import scrape_locations
from photo.scraper import scrape_photos

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()

    scheduler.add_job(scrape_locations, trigger=IntervalTrigger(days=5))
    scheduler.add_job(scrape_photos, trigger=IntervalTrigger(hours=5))

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass