# handlers/registration.py
from core.vk_client import send_message
from core.database import get_db
from keyboards.keyboards import (
    get_gender_keyboard,
    get_experience_keyboard,
    get_goal_keyboard,
    get_place_keyboard,
    get_split_keyboard,
    get_main_keyboard
)

def handle_registration(event, user_id):
    text = event.message.text.strip().lower() if event.message.text else ""

    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE vk_id=?", (user_id,)).fetchone()

        if not user:
            conn.execute("INSERT INTO users (vk_id, registered) VALUES (?, 0)", (user_id,))
            send_message(user_id, "Привет! Я фитнес-бот. Давай познакомимся. Как тебя зовут?")
            return

        if user["registered"] == 0:
            fields = ["name", "gender", "height", "weight", "experience", "goal", "place", "split"]
            for field in fields:
                current = user[field]
                if current is None or (field in ("height", "weight") and current == 0):
                    if field == "name":
                        conn.execute("UPDATE users SET name=? WHERE vk_id=?", (event.message.text, user_id))
                        send_message(user_id, "Выберите пол:", get_gender_keyboard())
                        return
                    elif field == "gender":
                        if "мужской" in text or "женский" in text:
                            gender = "мужской" if "мужской" in text else "женский"
                            conn.execute("UPDATE users SET gender=? WHERE vk_id=?", (gender, user_id))
                            send_message(user_id, "Введите ваш рост (в см):")
                        else:
                            send_message(user_id, "Пожалуйста, выберите пол кнопкой.")
                        return
                    elif field == "height":
                        if text.isdigit() and 50 < int(text) < 250:
                            conn.execute("UPDATE users SET height=? WHERE vk_id=?", (int(text), user_id))
                            send_message(user_id, "Введите ваш вес (в кг):")
                        else:
                            send_message(user_id, "Введите реальный рост в см (50-250).")
                        return
                    elif field == "weight":
                        if text.isdigit() and 30 < int(text) < 350:
                            conn.execute("UPDATE users SET weight=? WHERE vk_id=?", (int(text), user_id))
                            send_message(user_id, "Ваш стаж тренировок:", get_experience_keyboard())
                        else:
                            send_message(user_id, "Введите реальный вес в кг (30-350).")
                        return
                    elif field == "experience":
                        if any(kw in text for kw in ["новичок", "средний", "опытный"]):
                            if "новичок" in text:
                                exp = "новичок"
                            elif "средний" in text:
                                exp = "средний"
                            else:
                                exp = "опытный"
                            conn.execute("UPDATE users SET experience=? WHERE vk_id=?", (exp, user_id))
                            send_message(user_id, "Выберите цель тренировок:", get_goal_keyboard())
                        else:
                            send_message(user_id, "Выберите стаж кнопкой.")
                        return
                    elif field == "goal":
                        if any(kw in text for kw in ["похудение", "набор массы", "рельеф", "поддержка формы"]):
                            if "похудение" in text:
                                goal = "похудение"
                            elif "набор массы" in text:
                                goal = "набор массы"
                            elif "рельеф" in text:
                                goal = "рельеф"
                            else:
                                goal = "поддержка формы"
                            conn.execute("UPDATE users SET goal=? WHERE vk_id=?", (goal, user_id))
                            send_message(user_id, "Где планируете заниматься?", get_place_keyboard())
                        else:
                            send_message(user_id, "Выберите цель кнопкой.")
                        return
                    elif field == "place":
                        if "зал" in text or "дома" in text:
                            place = "зал" if "зал" in text else "дома"
                            conn.execute("UPDATE users SET place=? WHERE vk_id=?", (place, user_id))
                            send_message(user_id, "Выберите тип сплита:", get_split_keyboard())
                        else:
                            send_message(user_id, "Выберите место кнопкой.")
                        return
                    elif field == "split":
                        if any(kw in text for kw in ["фулбоди", "верх/низ", "трёхдневный сплит"]):
                            if "фулбоди" in text:
                                split = "фулбоди"
                            elif "верх/низ" in text:
                                split = "верх/низ"
                            else:
                                split = "трёхдневный сплит"
                            conn.execute("UPDATE users SET split=? WHERE vk_id=?", (split, user_id))
                            conn.execute("UPDATE users SET registered=1 WHERE vk_id=?", (user_id,))
                            send_message(user_id, "Регистрация завершена! Добро пожаловать.", get_main_keyboard())
                        else:
                            send_message(user_id, "Выберите сплит кнопкой.")
                        return
        else:
            send_message(user_id, "Вы уже зарегистрированы. Используйте меню.", get_main_keyboard())