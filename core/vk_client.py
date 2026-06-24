import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import settings

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=settings.GROUP_ID)

def send_message(user_id, message, keyboard=None, attachment=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard,
        attachment=attachment
    )