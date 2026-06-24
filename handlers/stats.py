from core.vk_client import send_message
from services.stats_service import get_user_stats
from services.achievement_service import check_achievements
from keyboards.keyboards import get_main_keyboard
import calendar
from datetime import datetime
from core.database import get_db

def generate_calendar(vk_id):
    today = datetime.now()
    year, month = today.year, today.month
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    with get_db() as conn:
        rows = conn.execute(
            "SELECT date FROM training_log WHERE user_id=? AND date >= ? AND date <= ?",
            (vk_id, f"{year}-{month:02d}-01", f"{year}-{month:02d}-31")
        ).fetchall()
    trained_days = set()
    for row in rows:
        try:
            d = datetime.strptime(row["date"], "%Y-%m-%d").day
            trained_days.add(d)
        except:
            pass

    month_name = today.strftime("%B %Y")
    cal_lines = [month_name.center(20, " ")]
    week_header = "Пн Вт Ср Чт Пт Сб Вс"
    cal_lines.append(week_header)

    for week in month_days:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            else:
                if day in trained_days:
                    line += f"✅{day:2d}"
                else:
                    line += f"⬜{day:2d}"
                line += " "
        cal_lines.append(line)

    return "```\n" + "\n".join(cal_lines) + "\n```"

def handle_stats(event, user_id):
    total, week, params = get_user_stats(user_id)
    achievements = check_achievements(user_id)
    ach_str = "\n".join(achievements) if achievements else "Пока нет достижений"
    calendar_view = generate_calendar(user_id)
    msg = (
        f"📊 Статистика:\n"
        f"Тренировок всего: {total}\n"
        f"За последнюю неделю: {week}\n"
        f"{params}\n\n"
        f"🏅 Достижения:\n{ach_str}\n\n"
        f"{calendar_view}"
    )
    send_message(user_id, msg, get_main_keyboard())