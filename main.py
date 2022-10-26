import vk_api
import pypresence
import configparser
import time
from chardet.universaldetector import UniversalDetector

print("Программа инициализируется...")

config = configparser.ConfigParser()
detector = UniversalDetector()
with open('config.ini', 'rb') as fh:
    for line in fh:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
config.read("config.ini", encoding=detector.result["encoding"])
app_id = '543726720289734656'


def run():
    try:
        presence = pypresence.Presence(app_id)
        presence.connect()
        vk_session = vk_api.VkApi(token=config['VK']['app_token'])
        vk = vk_session.get_api()

        print("Приложение было проинициализировано. Запуск через 5 секунд.")
        time.sleep(5)
        while True:
            large_image = "vk"
            activity = {
                "large_image": large_image
            }
            res = vk.users.get(user_ids=config['VK']['id'], fields="status")[0]
            print(res)

            if "status_audio" not in res:
                state = "Музыка не воспроизводится"
                if "details" in activity:
                    activity.pop("details")

                large_image = 'vk'
                activity.update({'state': state, 'large_image': large_image})
            else:
                curr_music = res['status_audio']

                state = f"Автор - {curr_music['artist']}"
                details = f"Трек - {curr_music['title']}"
                if 'album' in curr_music and 'thumb' in curr_music['album']:
                    large_image = curr_music["album"]["thumb"]["photo_300"]

                activity.update(
                    {'state': state, 'details': details,
                     'large_image': large_image})

            presence.update(**activity)
            time.sleep(15)
    except OSError:
        print("fuck. Restarting.")
        run()


if __name__ == "__main__":
    run()
