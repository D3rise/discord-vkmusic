import vk_api
import rpc
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
        rpc_obj = rpc.DiscordIpcClient.for_platform(app_id)
        vk_session = vk_api.VkApi(token=config['VK']['app_token'])
        vk = vk_session.get_api()

        print("Приложение было проинициализировано. Запуск через 5 секунд.")
        time.sleep(5)
        while True:
            activity = {
                "assets": {
                    "large_image": "vk"
                }
            }
            res = vk.users.get(user_ids=config['VK']['id'], fields="status")[0]

            if "status_audio" not in res:
                state = "Музыка не воспроизводится"
                if "details" in activity:
                    activity.pop("details")

                activity.update({'state': state})
            else:
                curr_music = vk.users.get(user_ids=config['VK']['id'], fields="status")[0]['status_audio']
                state = f"Автор - {curr_music['artist']}"
                details = f"Трек - {curr_music['title']}"
                activity.update({'state': state, 'details': details})

            rpc_obj.set_activity(activity)
            time.sleep(15)
    except OSError:
        print("fuck. Restarting.")
        run()


if __name__ == "__main__":
    run()
