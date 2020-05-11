#!/usr/bin/python3

import requests
from configparser import ConfigParser

parser = ConfigParser()
parser.read("settings.ini")

BOT_TOKEN = parser.get("telegram", "BOT_TOKEN")
CHAT_ID = parser.get("telegram", "CHAT_ID")
NOTIFIER = parser.get("settings", "NOTIFIER")


def notifier(message, programs):
    if NOTIFIER == "telegram":
        telegram(message, programs)
    else:
        print(
            "Error: No valid notifier was specified. Please check your 'settings.ini' file"
        )


def telegram(message, programs):
    print("sending message through telegram")
    programs_as_string = ""
    for i in programs:
        programs_as_string += i
        programs_as_string += "\n"
    print(programs_as_string)
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    r = requests.post(
        url, data={"chat_id": CHAT_ID, "text": message + programs_as_string}
    )


def notify(res, programs):
    if res is 0:
        notifier("✅ All the programs are up to date. \n", '')
    elif res is 1:
        notifier("⚠️ The following program(s) require an update: \n", programs)
    else:
        print("The build status could not be retrieved")
