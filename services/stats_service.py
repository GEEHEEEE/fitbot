from core.database import get_db
from datetime import datetime, timedelta

def get_user_stats(vk_id):
    with get_db() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM training_log WHERE user_id=?",
            (vk_id,)
        ).fetchone()[0]

        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        week = conn.execute(
            "SELECT COUNT(*) FROM training_log WHERE user_id=? AND date >= ?",
            (vk_id, week_ago)
        ).fetchone()[0]

        user = conn.execute(
            "SELECT * FROM users WHERE vk_id=?", (vk_id,)
        ).fetchone()
        if user:
            params = (
                f"Рост: {user['height']} см, Вес: {user['weight']} кг, "
                f"Стаж: {user['experience']}"
            )
        else:
            params = "Данные не найдены"

    return total, week, params