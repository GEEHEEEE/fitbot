from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from datetime import datetime
from utils.logger import setup_logger
from core.database import get_db
from core.vk_client import send_message
from keyboards.keyboards import get_main_keyboard

logger = setup_logger()
scheduler = BackgroundScheduler()

def start_scheduler():
    with get_db() as conn:
        users = conn.execute(
            "SELECT vk_id, reminder_time, timezone FROM users WHERE reminder_time IS NOT NULL"
        ).fetchall()
        for user in users:
            if user["reminder_time"]:
                try:
                    tz = pytz.timezone(user["timezone"])
                    hour, minute = map(int, user["reminder_time"].split(":"))
                    scheduler.add_job(
                        send_reminder,
                        trigger=CronTrigger(hour=hour, minute=minute, timezone=tz),
                        args=[user["vk_id"]],
                        id=f"reminder_{user['vk_id']}",
                        replace_existing=True
                    )
                except Exception as e:
                    logger.error(
                        f"Не удалось добавить напоминание для {user['vk_id']}: {e}"
                    )
    scheduler.start()
    logger.info("Планировщик запущен")

def send_reminder(user_id):
    try:
        send_message(user_id, "⏰ Время тренировки! Пора заниматься!",
                     get_main_keyboard())
        logger.info(f"Отправлено напоминание пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания пользователю {user_id}: {e}")