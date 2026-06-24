from config import settings
from core.database import init_db
from core.vk_client import longpoll, send_message
from core.rate_limiter import rate_limiter
from core.scheduler import start_scheduler
from core.user_states import get_state
from handlers import (
    handle_registration,
    handle_training,
    handle_nutrition,
    handle_stats,
    handle_settings
)
from keyboards.keyboards import get_main_keyboard
from utils.logger import setup_logger
from vk_api.bot_longpoll import VkBotEventType

logger = setup_logger()

def is_registered(user_id):
    from core.database import get_db
    with get_db() as conn:
        user = conn.execute("SELECT registered FROM users WHERE vk_id=?", (user_id,)).fetchone()
        return user is not None and user["registered"] == 1

def main():
    logger.info("Запуск бота")
    init_db()
    start_scheduler()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.message.from_id
            if not rate_limiter.is_allowed(user_id):
                logger.warning(f"Rate limit exceeded for user {user_id}")
                continue

            text = event.message.text.strip() if event.message.text else ""
            if not text:
                continue
            text_lower = text.lower()

            try:
                if get_state(user_id):
                    handle_settings(event, user_id)
                    continue

                if not is_registered(user_id) or any(kw in text_lower for kw in ["начать", "старт"]):
                    handle_registration(event, user_id)
                    continue

                if "программа тренировок" in text_lower or "отметить тренировку" in text_lower:
                    handle_training(event, user_id)
                    continue

                if "питание" in text_lower or "завтрак" in text_lower or "обед" in text_lower or \
                   "ужин" in text_lower or "рекомендации" in text_lower or "назад в меню" in text_lower:
                    handle_nutrition(event, user_id)
                    continue

                if "статистика" in text_lower:
                    handle_stats(event, user_id)
                    continue

                if any(kw in text_lower for kw in [
                    "настройки", "изменить имя", "изменить пол", "изменить рост", "изменить вес",
                    "изменить стаж", "изменить цель", "изменить место", "изменить сплит",
                    "напоминания", "назад в настройки", "установить напоминание", "отключить напоминание",
                    "мужской", "женский", "новичок", "средний", "опытный",
                    "похудение", "набор массы", "рельеф", "поддержка формы",
                    "зал", "дома", "фулбоди", "верх/низ", "трёхдневный сплит"
                ]):
                    handle_settings(event, user_id)
                    continue

                send_message(user_id, "Используйте кнопки меню.", get_main_keyboard())

            except Exception as e:
                logger.error(f"Ошибка обработки сообщения от {user_id}: {e}", exc_info=True)
                send_message(user_id, "Произошла ошибка. Попробуйте позже.")

if __name__ == "__main__":
    main()