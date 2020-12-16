import subprocess
import time

from bot_handler import BotHandler
from dotenv import load_dotenv
import os
import datetime
import loguru
import pycbrf
import numpy as np
import cv2

if os.name != 'nt':
    import alsaaudio

load_dotenv()
token = os.getenv('MY_TOKEN')

greet_bot = BotHandler(token)
greetings_list = ('hello', '/hi', 'qq', 'greetings')
currency_list = ("eur", "usd")
currency_list_correct = ("EUR", "USD")
bot_key = '/'
now = datetime.datetime.now()
admin_id = '388863805'
valid_chats = [388863805, -259505319, -342305508]
admin_commands_list = ['/add_chat_id', '/show_active_chats']
volume_commands = ['звук', 'volume', 'громкость', 'vol', 'v']
photo_commands = ['p', 'photo', 'take_photo', 'фото', 'сфотографируй']


def main():
    loguru.logger.add('log.log')
    loguru.logger.debug("Start main")

    new_offset = None
    today = now.day
    hour = now.hour

    if os.name != 'nt':
        m = alsaaudio.Mixer('Headphone')
        current_volume = m.getvolume()
        m.setvolume(0)
        loguru.logger.debug(f'current volume is set from {current_volume} to {0}')

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        if not last_update:
            continue

        loguru.logger.debug(last_update)
        last_update_id = last_update['update_id']
        if 'text' not in last_update['message'].keys():
            new_offset = last_update_id + 1
            continue
        else:
            last_chat_text = last_update['message']['text']
        # try:
        #
        # except KeyError:
        #     new_offset = last_update_id + 1
        #     continue
        last_chat_id = last_update['message']['chat']['id']
        if last_chat_id not in valid_chats:
            new_offset = last_update_id + 1
            continue
        # if 'first_name' in last_update['message']['chat']:
        #     last_private_chat_name = last_update['message']['chat']['first_name']
        # else:
        #     last_chat_name = last_update['message']['from']['first_name']
        last_message_sender_name = last_update['message']['from']['first_name']
        message = last_chat_text.lower()
        if bot_key in message:
            if message == bot_key:
                greet_bot.send_message(last_chat_id, f"Waiting for commends")
                continue
            cmd = message.split(bot_key)[1].split(' ')[0]
            if len(message.split(bot_key)[1].split(' ')) > 1:
                param = message.split(bot_key)[1].split(' ')[1]
            else:
                param = None
            if cmd in greetings_list:
                if 6 <= hour < 12:
                    greet_bot.send_message(last_chat_id, f"Доброе утро, {last_message_sender_name}")
                elif 12 <= hour < 18:
                    greet_bot.send_message(last_chat_id, f"Добрый день, {last_message_sender_name}")
                elif 18 <= hour < 23:
                    greet_bot.send_message(last_chat_id, f"Добрый вечер, {last_message_sender_name}")
            elif cmd in currency_list:
                currency = currency_list[currency_list.index(cmd)]
                rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                currency_name = currency_list_correct[currency_list.index(currency)]
                loguru.logger.debug(currency_name)
                greet_bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB")
            # for currency in currency_list:
            #     if currency in last_chat_text.lower():
            #         rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
            #         currency_name = currency_list_correct[currency_list.index(currency)]
            #         loguru.logger.debug(currency_name)
            #         greet_bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB")

            elif cmd in volume_commands:
                if os.name != 'nt':
                    loguru.logger.debug("Управление звуком зарегистрировано")
                    volume = param
                    if volume.isdigit():
                        int_volume = int(volume)
                        if int_volume > 150:
                            m.setvolume(150)
                            greet_bot.send_message(last_chat_id,
                                                   f"Ставлю звук на максимум")
                        elif int_volume < 0:
                            m.setvolume(0)
                            greet_bot.send_message(last_chat_id,
                                                   f"Выключаю звук")
                        else:
                            m.setvolume(int_volume)
                            greet_bot.send_message(last_chat_id,
                                                   f"Ставлю звук на {int_volume}")
                    else:
                        m.setvolume(0)
                        greet_bot.send_message(last_chat_id,
                                               f"Команда не распознана до конца, выключаю звук")

                else:
                    greet_bot.send_message(last_chat_id,f"Не та ОС")

            elif cmd in photo_commands:
                photo_name = f'/home/pi/smart-home/camera_1_photos/{datetime.datetime.now().strftime("%d%m%Y-%H%M")}.png'
                # subprocess.call(f'fswebcam -q -r 1280x720 {photo_name}', shell=True)
                if param is None:
                    cam = 0
                else:
                    cam = param
                cap = cv2.VideoCapture(cam)
                ret,frame = cap.read()
                cv2.imshow('img1', frame)
                cv2.imwrite(photo_name, frame)
                cv2.destroyAllWindows()
                cap.release()
                if os.path.exists(photo_name):
                    greet_bot.send_photo(last_chat_id, photo_name)
                else:
                    greet_bot.send_message(last_chat_id, f"Ошибка с формированием и отправкой фото")
        new_offset = last_update_id + 1
        loguru.logger.debug(new_offset)


if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            exit()
        except:
            time.sleep(15)
