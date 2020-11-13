from my_bot.bot_handler import BotHandler
from dotenv import load_dotenv
import os
import datetime
import loguru
import pycbrf


load_dotenv()
token = os.getenv('MY_TOKEN')

greet_bot = BotHandler(token)
greetings_list = ('hello', '/hi', 'qq', 'greetings')
currency_list = ("/евро", "/доллар")
currency_list_correct = ("EUR", "USD")
now = datetime.datetime.now()
admin_id = '388863805'
valid_chats = [388863805, -259505319]
admin_commands_list = ['/add_chat_id', '/show_active_chats']


def main():
    loguru.logger.debug("Start main")
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        if not last_update:
            loguru.logger.debug("Nothing to update")
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
        if last_chat_text.lower() in greetings_list and today == now.day:
            if 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, f"Доброе утро, {last_message_sender_name}")
            elif 12 <= hour < 18:
                greet_bot.send_message(last_chat_id, f"Добрый день, {last_message_sender_name}")
            elif 18 <= hour < 23:
                greet_bot.send_message(last_chat_id, f"Добрый вечер, {last_message_sender_name}")
        for currency in currency_list:
            if currency in last_chat_text.lower():
                rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                currency_name = currency_list_correct[currency_list.index(currency)]
                loguru.logger.debug(currency_name)
                greet_bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB")
        new_offset = last_update_id + 1
        loguru.logger.debug(new_offset)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
