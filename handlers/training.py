# handlers/training.py
import os
from core.vk_client import send_message, vk, vk_session   # <-- добавили vk_session
from core.database import get_db
from services.training_service import get_program
from workout_generator import generate_excel
from utils.logger import setup_logger
from keyboards.keyboards import get_main_keyboard

logger = setup_logger()

def handle_training(event, user_id):
    text = event.message.text.strip().lower() if event.message.text else ""
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE vk_id=?", (user_id,)).fetchone()
        if not user or user["registered"] == 0:
            send_message(user_id, "Сначала завершите регистрацию.")
            return

    if "программа тренировок" in text:
        program = get_program(user["goal"], user["place"], user["split"])
        if "error" in program:
            send_message(user_id, program["error"])
            return

        os.makedirs("cache", exist_ok=True)
        filepath = f"cache/workout_{user_id}.xlsx"

        try:
            generate_excel(program, filepath)

            # 1. Получаем URL для загрузки
            upload_data = vk.docs.getMessagesUploadServer(type="doc", peer_id=user_id)
            upload_url = upload_data['upload_url']

            # 2. Загружаем файл через сессию vk_api (правильный HTTP-клиент)
            with open(filepath, 'rb') as f:
                response = vk_session.http.post(upload_url, files={'file': f})

            # 3. Проверяем ответ
            if response.status_code != 200:
                logger.error(
                    f"Ошибка загрузки файла. Статус: {response.status_code}, Тело: {response.text[:200]}"
                )
                raise Exception("Сервер ВКонтакте не принял файл")

            try:
                upload_result = response.json()
            except Exception as json_err:
                logger.error(f"Некорректный JSON от сервера загрузки: {response.text[:200]}")
                raise Exception("Некорректный ответ сервера при загрузке файла")

            if 'file' not in upload_result:
                logger.error(f"В ответе на загрузку отсутствует 'file': {upload_result}")
                raise Exception("Не удалось загрузить файл на сервер ВК")

            # 4. Сохраняем документ
            doc = vk.docs.save(file=upload_result['file'], title='Программа тренировок на месяц')['doc']
            send_message(user_id, "Ваша программа тренировок на месяц:",
                         attachment=f"doc{doc['owner_id']}_{doc['id']}")

        except Exception as e:
            logger.error(f"Ошибка отправки Excel: {e}")
            # Fallback – текстовая версия первой недели
            week1 = get_program(user["goal"], user["place"], user["split"], week=1)
            if "weeks" in week1 and week1["weeks"]:
                days = week1["weeks"][0]["days"]
                text_program = "\n".join(
                    [f"{d['day_name']}:\n" +
                     "\n".join([f"- {ex['exercise']}: {ex['sets']}x{ex['reps']}" for ex in d['exercises']])
                     for d in days]
                )
                send_message(user_id, f"Программа (текст):\n{text_program}", get_main_keyboard())
            else:
                send_message(user_id, "Не удалось сформировать программу.")

    elif "отметить тренировку" in text:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            conn.execute("INSERT INTO training_log (user_id, date) VALUES (?, ?)", (user_id, today))
        send_message(user_id, "Тренировка отмечена! Так держать! 💪", get_main_keyboard())