from apscheduler.schedulers.background import BackgroundScheduler

from app.services.gmail.history_monitor import HistoryMonitor

scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.start()

    monitor = HistoryMonitor()

    scheduler.add_job(

        monitor.run,

        "interval",

        seconds=30,

        id="gmail-monitor",

        replace_existing=True,

        max_instances=1,

    )

    print("✅ Scheduler Started")