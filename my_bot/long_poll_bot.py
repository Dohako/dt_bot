from my_bot.bot_handler import BotHandler
from dotenv import load_dotenv
import os
import datetime
import loguru
import pycbrf


load_dotenv()
token = os.getenv('MY_TOKEN')

greet_bot = BotHandler(token)
greetings_list = ('hello', 'hi', 'qq', 'greetings')
currency_list = ("евро", "доллар")
currency_list_correct = ("EUR", "USD")
now = datetime.datetime.now()


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

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        loguru.logger.debug(f"today is {today}, hour is {hour}")
        if last_chat_text.lower() in greetings_list and today == now.day:
            if 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, f"Доброе утро, {last_chat_name}")
            elif 12 <= hour < 18:
                greet_bot.send_message(last_chat_id, f"Добрый день, {last_chat_name}")
            elif 18 <= hour < 23:
                greet_bot.send_message(last_chat_id, f"Добрый вечер, {last_chat_name}")
        for currency in currency_list:
            if currency in last_chat_text.lower():
                rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                currency_name = currency_list_correct[currency_list.index(currency)]
                loguru.logger.debug(currency_name)
                greet_bot.send_message(last_chat_id, f"1 {currency} = {rates[currency_name].value} руб")
        new_offset = last_update_id + 1
        loguru.logger.debug(new_offset)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
