from apscheduler.schedulers.blocking import BlockingScheduler
from bot import main

schedule = BlockingScheduler()


@schedule.scheduled_job('cron', day_of_week='mon,tue,wed,thu,fri,sat,sun', hour=8, timezone='America/Sao_Paulo')
def scheduled_job():
    main()


schedule.start()