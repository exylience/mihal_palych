from os import read
import vk_api

from random import randint
import json

from vk_api import longpoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

# API token
TOKEN = "7acbc17a73baad4d0285bf07f8c3202d15745100da5077f64cafadf4ee858f3e83ff289f77f6cb3c1a61c"

# авторизуемся как сообщество
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# сетевой демон для работы с сообщениями
longpoll = VkLongPoll(vk_session)


upload = vk_api.VkUpload(vk)

keyboard = VkKeyboard(one_time = False)
keyboard.add_button("драйв", color = VkKeyboardColor.POSITIVE)


with open("assets/allowed_pick.json", "r", encoding="utf-8") as read_file:
    allowed_pick = json.load(read_file)
    allowed_pick = allowed_pick.get("data")
    read_file.close()

with open("assets/banned_pick.json", "r", encoding="utf-8") as read_file:
    banned_pick = json.load(read_file)
    banned_pick = banned_pick.get("data")
    read_file.close()

def test_reply(event):
    if event.to_me:
        vk.messages.send(
            message="ответ",
            key=("9336ef10bd5469381c84f831f563f8b7fb8bd567"),
            server=("https://lp.vk.com/wh170215431"),
            ts=("38986"),
            random_id=vk_api.utils.get_random_id(),
            user_id=event.user_id
        )

def reply_to_tiktok(event):
    if event.from_chat:
        vk.messages.send(
            message="",
            attachment="photo-170215431_457239023",
            key=("9336ef10bd5469381c84f831f563f8b7fb8bd567"),
            server=("https://lp.vk.com/wh170215431"),
            ts=("38986"),
            random_id=vk_api.utils.get_random_id(),
            chat_id=event.chat_id
        )

def santa(event):
    if event.object.from_id in banned_pick:
        vk.messages.send(
            message="а я чет не понял, ты че сука, ты че выебываешься?",
            key=('9336ef10bd5469381c84f831f563f8b7fb8bd567'),
            server=("https://lp.vk.com/wh170215431"),
            ts=("38986"),
            random_id=vk_api.utils.get_random_id(),
            user_id=event.user_id
        )
    else:
        random_person_index = randint(0, len(allowed_pick) - 1)

        random_person = allowed_pick[random_person_index]

        random_person_id = random_person.get("user_id")
        random_person_name = random_person.get("name")

        photo = upload.photo_messages(random_person.get("image_url"))
        owner_id = photo[0]["owner_id"]
        photo_id = photo[0]["id"]
        access_key = photo[0]["access_key"]

        attachment = f"photo{owner_id}_{photo_id}_{access_key}"

        del allowed_pick[random_person_index]

        with open("assets/allowed_pick.json", "w") as read_file:
            dict = { "data": allowed_pick }
            json.dump(dict, read_file, ensure_ascii=False)
            read_file.close()

        banned_pick.append(event.object.from_id)

        with open("assets/banned_pick.json", "w", encoding="utf-8") as read_file:
            dict = { "data": banned_pick }
            json.dump(dict, read_file, ensure_ascii=False)
            read_file.close()

        if event.to_me:
            vk.messages.send(
                message=f"@id{random_person_id} ({random_person_name})",
                attachment=attachment,
                key=("9336ef10bd5469381c84f831f563f8b7fb8bd567"),
                server=("https://lp.vk.com/wh170215431"),
                ts=("38986"),
                random_id=vk_api.utils.get_random_id(),
                user_id=event.user_id
            )
    

# запускаем сетевого демона
for event in longpoll.listen():
    # если пришло сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        message = str(event.text).split(".")
        
        if 'tiktok' in message or 'tiktok' in str(event) or 'тик ток' in str(event):
            reply_to_tiktok(event)

        if "драйв" in str(event):
            santa(event)

        if "test" in str(event.text):
            test_reply(event)



