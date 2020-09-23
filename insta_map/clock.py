if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(pics, trigger=RandomIntervalTrigger(hours=5, minutes=55, seconds=59, timezone="Europe/Rome"))
    scheduler.add_job(itookapic, trigger=RandomIntervalTrigger(hours=5, minutes=55, seconds=59, timezone="Europe/Rome"))
    scheduler.add_job(quotes, trigger=RandomIntervalTrigger(hours=4, minutes=55, seconds=59, timezone="Europe/Rome"))
    scheduler.add_job(stories, trigger=RandomIntervalTrigger(hours=4, minutes=55, seconds=59, timezone="Europe/Rome"))
    scheduler.add_job(verses, trigger=RandomIntervalTrigger(hours=4, minutes=55, seconds=59, timezone="Europe/Rome"))
    scheduler.add_job(facts, trigger=RandomIntervalTrigger(hours=4, minutes=55, seconds=59, timezone="Europe/Rome"))

    notification = ""
    for job in scheduler.get_jobs():
        notification += job.func_ref + str(job.trigger.interval) + ', '

    requests.post(
        "https://discordapp.com/api/webhooks/652499253515649040/yS3AauwtwZNeZdMRTqx-p_jk0bG2e5jR-WtbsTC9nuLYwbNVrl-WLhL6UqKFaNGIvfJn",
        data={
            'content': notification
        }
    )

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass