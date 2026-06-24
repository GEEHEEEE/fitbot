from core.database import get_db

ACHIEVEMENTS = {
    5: "🥉 Новичок",
    10: "🥈 Любитель",
    20: "🥇 Атлет",
    50: "🏆 Чемпион",
    100: "💪 Легенда"
}

def check_achievements(vk_id):
    with get_db() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM training_log WHERE user_id=?",
            (vk_id,)
        ).fetchone()[0]

    earned = []
    for threshold, name in sorted(ACHIEVEMENTS.items()):
        if total >= threshold:
            earned.append(f"{name} ({threshold} тренировок)")
    return earned