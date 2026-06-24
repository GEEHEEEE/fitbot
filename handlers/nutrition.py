from core.vk_client import send_message
from core.database import get_db
from data.nutrition_data import meals, nutrition_tips, sport_nutrition_tips
from keyboards.keyboards import get_nutrition_keyboard, get_main_keyboard

def handle_nutrition(event, user_id):
    text = event.message.text.strip().lower() if event.message.text else ""
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE vk_id=?", (user_id,)).fetchone()
        if not user or user["registered"] == 0:
            send_message(user_id, "Сначала завершите регистрацию.")
            return

    goal = user["goal"]

    if "питание" in text:
        send_message(user_id, "Выберите приём пищи или рекомендации:", get_nutrition_keyboard())
    elif "завтрак" in text:
        msg = "🥞 **Завтрак (на выбор):**\n" + "\n".join(
            [f"{m['name']} — {m['calories']} ккал, Б:{m['protein']}г, Ж:{m['fat']}г, У:{m['carbs']}г" for m in meals["breakfast"]]
        )
        send_message(user_id, msg, get_nutrition_keyboard())
    elif "обед" in text:
        msg = "🍲 **Обед (на выбор):**\n" + "\n".join(
            [f"{m['name']} — {m['calories']} ккал, Б:{m['protein']}г, Ж:{m['fat']}г, У:{m['carbs']}г" for m in meals["lunch"]]
        )
        send_message(user_id, msg, get_nutrition_keyboard())
    elif "ужин" in text:
        msg = "🥗 **Ужин (на выбор):**\n" + "\n".join(
            [f"{m['name']} — {m['calories']} ккал, Б:{m['protein']}г, Ж:{m['fat']}г, У:{m['carbs']}г" for m in meals["dinner"]]
        )
        send_message(user_id, msg, get_nutrition_keyboard())
    elif "рекомендации" in text:
        general = nutrition_tips.get(goal, "Сбалансированное питание важно!")
        sport = sport_nutrition_tips.get(goal, "")
        send_message(user_id, f"{general}\n\n{sport}", get_nutrition_keyboard())
    elif "назад в меню" in text:
        send_message(user_id, "Главное меню", get_main_keyboard())
    else:
        send_message(user_id, "Пожалуйста, выберите кнопкой из меню питания.", get_nutrition_keyboard())