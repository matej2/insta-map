import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from insta_map.common import save_proxies

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()

    #scheduler.add_job(save_proxies, trigger=IntervalTrigger(days=1))

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass