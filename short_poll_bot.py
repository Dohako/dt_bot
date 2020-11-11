from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
MY_TOKEN = os.getenv("MY_TOKEN")

url = f"https://api.telegram.org/bot{MY_TOKEN}/"


def get_updates_json(request):
    params = {'timeout' : 100, 'offset' : None}
    response = requests.get(request + 'getUpdates',data=params)
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def send_message(chat,text):
    params = {'chat_id' : chat, 'text' : text}
    response = requests.post(url + 'SendMessage', data=params)
    return response


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            send_message(get_chat_id(last_update(get_updates_json(url))),'test')
            update_id += 1
        time.sleep(1)

if __name__ == '__main__':
    main()
#
# chat_id = get_chat_id(last_update(get_updates_json(url)))
# send_message(chat_id,'Hello')