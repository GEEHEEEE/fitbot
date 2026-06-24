# keyboards/keyboards.py
import json

def get_empty_keyboard():
    return json.dumps({"one_time": False, "buttons": []})

def get_main_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "🏋️ Программа тренировок"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🥗 Питание"}, "color": "default"}],
        [{"action": {"type": "text", "label": "📊 Статистика"}, "color": "default"}],
        [{"action": {"type": "text", "label": "✅ Отметить тренировку"}, "color": "positive"}],
        [{"action": {"type": "text", "label": "⚙️ Настройки"}, "color": "default"}]
    ]
    return json.dumps({"one_time": False, "buttons": buttons})

def get_gender_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "🚹 Мужской"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🚺 Женский"}, "color": "primary"}]
    ]
    return json.dumps({"one_time": True, "buttons": buttons})

def get_experience_keyboard():
    options = ["🌱 Новичок", "🌿 Средний", "🌳 Опытный"]
    buttons = [[{"action": {"type": "text", "label": opt}, "color": "default"}] for opt in options]
    return json.dumps({"one_time": True, "buttons": buttons})

def get_goal_keyboard():
    options = ["🔥 Похудение", "💪 Набор массы", "✨ Рельеф", "🧘 Поддержка формы"]
    buttons = [[{"action": {"type": "text", "label": opt}, "color": "default"}] for opt in options]
    return json.dumps({"one_time": True, "buttons": buttons})

def get_place_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "🏢 Зал"}, "color": "default"}],
        [{"action": {"type": "text", "label": "🏠 Дома"}, "color": "default"}]
    ]
    return json.dumps({"one_time": True, "buttons": buttons})

def get_split_keyboard():
    options = ["🔄 Фулбоди", "⬆️⬇️ Верх/низ", "📆 Трёхдневный сплит"]
    buttons = [[{"action": {"type": "text", "label": opt}, "color": "default"}] for opt in options]
    return json.dumps({"one_time": True, "buttons": buttons})

# Новые клавиатуры
def get_nutrition_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "🥞 Завтрак"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🍲 Обед"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🥗 Ужин"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "📋 Рекомендации"}, "color": "default"}],
        [{"action": {"type": "text", "label": "🔙 Назад в меню"}, "color": "negative"}]
    ]
    return json.dumps({"one_time": True, "buttons": buttons})

def get_settings_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "✏️ Изменить имя"}, "color": "default"}],
        [{"action": {"type": "text", "label": "🚻 Изменить пол"}, "color": "default"}],
        [{"action": {"type": "text", "label": "📏 Изменить рост"}, "color": "default"}],
        [{"action": {"type": "text", "label": "⚖️ Изменить вес"}, "color": "default"}],
        [{"action": {"type": "text", "label": "📈 Изменить стаж"}, "color": "default"}],
        [{"action": {"type": "text", "label": "🎯 Изменить цель"}, "color": "default"}],
        [{"action": {"type": "text", "label": "📍 Изменить место"}, "color": "default"}],
        [{"action": {"type": "text", "label": "📅 Изменить сплит"}, "color": "default"}],
        [{"action": {"type": "text", "label": "⏰ Напоминания"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🔙 Назад в меню"}, "color": "negative"}]
    ]
    return json.dumps({"one_time": True, "buttons": buttons})

def get_reminder_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "⏰ Установить напоминание"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🔕 Отключить напоминание"}, "color": "negative"}],
        [{"action": {"type": "text", "label": "🔙 Назад в настройки"}, "color": "default"}]
    ]
    return json.dumps({"one_time": True, "buttons": buttons})