from core.database import get_db
from core.scheduler import scheduler, send_reminder
from apscheduler.triggers.cron import CronTrigger
import pytz

def set_reminder(vk_id, time_str, timezone_str):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET reminder_time=?, timezone=? WHERE vk_id=?",
            (time_str, timezone_str, vk_id)
        )
    try:
        scheduler.remove_job(f"reminder_{vk_id}")
    except:
        pass

    tz = pytz.timezone(timezone_str)
    hour, minute = map(int, time_str.split(":"))
    scheduler.add_job(
        send_reminder,
        trigger=CronTrigger(hour=hour, minute=minute, timezone=tz),
        args=[vk_id],
        id=f"reminder_{vk_id}",
        replace_existing=True
    )

def disable_reminder(vk_id):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET reminder_time=NULL WHERE vk_id=?",
            (vk_id,)
        )
    try:
        scheduler.remove_job(f"reminder_{vk_id}")
    except:
        pass