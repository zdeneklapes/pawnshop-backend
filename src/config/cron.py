from django_cron import CronJobBase, Schedule


class UpdateProductStatusCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "config.cron"  # a unique code

    def do(self):
        print("Cron")
