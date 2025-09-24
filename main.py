from apscheduler.schedulers.background import BackgroundScheduler
from app.model.Appointment import create_weekly_availability
from app.bot import bot


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=create_weekly_availability, trigger='cron', day_of_week='tue', hour=17, minute=46, second=10)
    scheduler.start() 
    bot.infinity_polling()
