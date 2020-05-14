#!/usr/bin/python3

import os
import click
import requests
from configparser import ConfigParser

parser = ConfigParser()
parser.read("settings.ini")

NOTIFIER = parser.get("settings", "NOTIFIER")

def prerequisites():
    global BOT_TOKEN 
    global CHAT_ID
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')

    if os.environ.get('BOT_TOKEN') is None:
        BOT_TOKEN = parser.get("telegram", "BOT_TOKEN")
    if os.environ.get('CHAT_ID') is None:
        CHAT_ID = parser.get("telegram", "CHAT_ID")
    if BOT_TOKEN == "your_bot_token":
        print("The Telegram token was not updated from it's default value.\nPlease consult the README.md for more details")
        exit()
    elif CHAT_ID == "your_chat_id":
        print("The Telegram chat id was not updated from it's default value.\nPlease consult the README.md for more details")
        exit()
    if NOTIFIER != "telegram":
        print(
            "Error: No valid notifier was specified. Please check your 'settings.ini' file"
        )
        exit()

def telegram(message, programs):
    print("\n\nsending message through telegram ...")
    programs_as_string = ""
    for i in programs:
        programs_as_string += i
        programs_as_string += "\n"
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    r = requests.post(
        url, data={"chat_id": CHAT_ID, "text": message + programs_as_string}
    )
    click.secho("message sent !", fg='green')


def notify(res, programs):
    prerequisites()
    if res is True:
        message = "✅ All the programs are up to date. \n"
    elif res is False:
        message = "⚠️ The following program(s) require an update: \n"
    telegram(message, programs)