# handlers/settings.py
from core.vk_client import send_message
from core.database import get_db
from core.user_states import set_state, clear_state, get_state
from services.reminder_service import set_reminder, disable_reminder
from keyboards.keyboards import (
    get_main_keyboard, get_settings_keyboard, get_reminder_keyboard,
    get_gender_keyboard, get_experience_keyboard, get_goal_keyboard,
    get_place_keyboard, get_split_keyboard
)

def handle_settings(event, user_id):
    text = event.message.text.strip().lower() if event.message.text else ""
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE vk_id=?", (user_id,)).fetchone()
        if not user:
            send_message(user_id, "Сначала зарегистрируйтесь.")
            return

    state = get_state(user_id)
    if state:
        if state == "awaiting_name":
            new_name = event.message.text.strip()
            with get_db() as conn:
                conn.execute("UPDATE users SET name=? WHERE vk_id=?", (new_name, user_id))
            clear_state(user_id)
            send_message(user_id, f"Имя изменено на {new_name}.", get_settings_keyboard())
            return
        elif state == "awaiting_height":
            if text.isdigit() and 50 < int(text) < 250:
                with get_db() as conn:
                    conn.execute("UPDATE users SET height=? WHERE vk_id=?", (int(text), user_id))
                clear_state(user_id)
                send_message(user_id, f"Рост изменён на {text} см.", get_settings_keyboard())
            else:
                send_message(user_id, "Введите реальный рост в см (50-250):")
            return
        elif state == "awaiting_weight":
            if text.isdigit() and 30 < int(text) < 350:
                with get_db() as conn:
                    conn.execute("UPDATE users SET weight=? WHERE vk_id=?", (int(text), user_id))
                clear_state(user_id)
                send_message(user_id, f"Вес изменён на {text} кг.", get_settings_keyboard())
            else:
                send_message(user_id, "Введите реальный вес в кг (30-350):")
            return
        elif state == "awaiting_reminder_time":
            if len(text) == 5 and text[2] == ':':
                tz = user['timezone'] if user['timezone'] else 'Europe/Moscow'
                set_reminder(user_id, text, tz)
                clear_state(user_id)
                send_message(user_id, f"Напоминание установлено на {text} ({tz}).", get_reminder_keyboard())
            else:
                send_message(user_id, "Формат времени: ЧЧ:ММ, например 18:00")
            return
        else:
            clear_state(user_id)

    # Определение по ключевым словам
    if "настройки" in text and "назад" not in text:
        msg = (
            f"Имя: {user['name']}\n"
            f"Пол: {user['gender']}\n"
            f"Рост: {user['height']} см\n"
            f"Вес: {user['weight']} кг\n"
            f"Стаж: {user['experience']}\n"
            f"Цель: {user['goal']}\n"
            f"Место: {user['place']}\n"
            f"Сплит: {user['split']}\n"
        )
        if user['reminder_time']:
            msg += f"Напоминание: {user['reminder_time']} ({user['timezone']})"
        else:
            msg += "Напоминание отключено"
        send_message(user_id, msg, get_settings_keyboard())
    elif "изменить имя" in text:
        set_state(user_id, "awaiting_name")
        send_message(user_id, "Введите новое имя:")
    elif "изменить пол" in text:
        send_message(user_id, "Выберите пол:", get_gender_keyboard())
    elif "изменить рост" in text:
        set_state(user_id, "awaiting_height")
        send_message(user_id, "Введите новый рост (в см):")
    elif "изменить вес" in text:
        set_state(user_id, "awaiting_weight")
        send_message(user_id, "Введите новый вес (в кг):")
    elif "изменить стаж" in text:
        send_message(user_id, "Выберите стаж:", get_experience_keyboard())
    elif "изменить цель" in text:
        send_message(user_id, "Выберите цель:", get_goal_keyboard())
    elif "изменить место" in text:
        send_message(user_id, "Выберите место:", get_place_keyboard())
    elif "изменить сплит" in text:
        send_message(user_id, "Выберите сплит:", get_split_keyboard())
    elif "напоминания" in text:
        send_message(user_id, "Управление напоминаниями:", get_reminder_keyboard())
    elif "назад в меню" in text:
        send_message(user_id, "Главное меню", get_main_keyboard())
    elif "назад в настройки" in text:
        send_message(user_id, "Настройки", get_settings_keyboard())
    # Обработка выбора пола/стажа/цели/места/сплита с очисткой от эмодзи
    elif "мужской" in text or "женский" in text:
        gender = "мужской" if "мужской" in text else "женский"
        with get_db() as conn:
            conn.execute("UPDATE users SET gender=? WHERE vk_id=?", (gender, user_id))
        send_message(user_id, f"Пол изменён на {gender}.", get_settings_keyboard())
    elif "новичок" in text or "средний" in text or "опытный" in text:
        if "новичок" in text:
            experience = "новичок"
        elif "средний" in text:
            experience = "средний"
        else:
            experience = "опытный"
        with get_db() as conn:
            conn.execute("UPDATE users SET experience=? WHERE vk_id=?", (experience, user_id))
        send_message(user_id, f"Стаж изменён на {experience}.", get_settings_keyboard())
    elif "похудение" in text or "набор массы" in text or "рельеф" in text or "поддержка формы" in text:
        if "похудение" in text:
            goal = "похудение"
        elif "набор массы" in text:
            goal = "набор массы"
        elif "рельеф" in text:
            goal = "рельеф"
        else:
            goal = "поддержка формы"
        with get_db() as conn:
            conn.execute("UPDATE users SET goal=? WHERE vk_id=?", (goal, user_id))
        send_message(user_id, f"Цель изменена на {goal}.", get_settings_keyboard())
    elif "зал" in text or "дома" in text:
        place = "зал" if "зал" in text else "дома"
        with get_db() as conn:
            conn.execute("UPDATE users SET place=? WHERE vk_id=?", (place, user_id))
        send_message(user_id, f"Место тренировок изменено на {place}.", get_settings_keyboard())
    elif "фулбоди" in text or "верх/низ" in text or "трёхдневный сплит" in text:
        if "фулбоди" in text:
            split = "фулбоди"
        elif "верх/низ" in text:
            split = "верх/низ"
        else:
            split = "трёхдневный сплит"
        with get_db() as conn:
            conn.execute("UPDATE users SET split=? WHERE vk_id=?", (split, user_id))
        send_message(user_id, f"Сплит изменён на {split}.", get_settings_keyboard())
    elif "установить напоминание" in text:
        set_state(user_id, "awaiting_reminder_time")
        send_message(user_id, "Введите время напоминания в формате ЧЧ:ММ (например, 18:00):")
    elif "отключить напоминание" in text:
        disable_reminder(user_id)
        send_message(user_id, "Напоминание отключено.", get_reminder_keyboard())
    else:
        send_message(user_id, "Используйте кнопки настроек.", get_settings_keyboard())