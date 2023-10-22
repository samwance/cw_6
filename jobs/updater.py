from apscheduler.schedulers.background import BackgroundScheduler

from jobs.jobs import send_mailing


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=5)
    scheduler.start()
