from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def add_job(self, job_id, func, trigger="interval", **kwargs):
        if job_id in self.jobs:
            self.remove_job(job_id)
        job = self.scheduler.add_job(func, trigger, **kwargs)
        self.jobs[job_id] = job
        return job

    def remove_job(self, job_id):
        if job_id in self.jobs:
            self.scheduler.remove_job(self.jobs[job_id].id)
            del self.jobs[job_id]

    def list_jobs(self):
        return self.scheduler.get_jobs()

# Example usage
def my_task():
    print("Task executed at", datetime.now())
