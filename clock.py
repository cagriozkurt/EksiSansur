from apscheduler.schedulers.blocking import BlockingScheduler
from tools.database_tools import update_database

sched = BlockingScheduler()


@sched.scheduled_job("interval", hours=24)
def timed_job():
    print("Updating database...")
    update_database()


sched.start()
