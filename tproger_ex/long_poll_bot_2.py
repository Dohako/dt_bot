from dotenv import load_dotenv
import os
import datetime
import loguru
import requests


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        loguru.logger.debug(get_result)
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)] # Странный момент, зачем так?
        loguru.logger.debug(last_update)
        return last_update


load_dotenv()
token = os.getenv('MY_TOKEN')

greet_bot = BotHandler(token)
greetings = ('hello','hi','qq','greetings')
now = datetime.datetime.now()


def main():
    loguru.logger.debug("Start main")
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        loguru.logger.debug(f"today is {today}, hour is {hour}")
        if last_chat_text.lower() in greetings and today == now.day:
            if 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, f"Доброе утро, {last_chat_name}")
            elif 12 <= hour < 18:
                greet_bot.send_message(last_chat_id, f"Добрый день, {last_chat_name}")
            elif 18 <= hour < 23:
                greet_bot.send_message(last_chat_id, f"Добрый вечер, {last_chat_name}")
            today += 1 # таким образом за день будет отправлено только одно сообщение в ответ?
        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
