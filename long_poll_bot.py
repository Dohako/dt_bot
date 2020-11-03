from bot_handler import BotHandler
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
token = os.getenv('MY_TOKEN')

greet_bot = BotHandler(token)
greetings = ('hello','hi','qq','greetings')
now = datetime.datetime.now()

def main():
    pass