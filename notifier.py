#!/usr/bin/python3

import os
import click
import requests
from configparser import ConfigParser

parser = ConfigParser()
try:
    parser.read("settings.ini")
except Exception as e:
    error("Error: The config file could not be validated.\nPlease check that the file exists and is valid")
    raise SystemExit("")

def default(message):
    click.secho(message, fg='white')

def warning(message):
    click.secho(message, fg='blue', blink=True, bold=True)

def error(message):
    click.secho(message, fg='red')

def prerequisites():
    global BOT_TOKEN
    global CHAT_ID
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")
    NOTIFIER = os.environ.get("NOTIFIER")

    if os.environ.get("BOT_TOKEN") is None:
        try:
            BOT_TOKEN = parser.get("telegram", "BOT_TOKEN")
        except Exception as e:
            error("\nError: The config file could not be validated.\nPlease check that the file exists and is valid")
            raise SystemExit("")
    if os.environ.get("CHAT_ID") is None:
        try:
            CHAT_ID = parser.get("telegram", "CHAT_ID")
        except Exception as e:
            error("\nError: The config file could not be validated.\nPlease check that the file exists and is valid")
            raise SystemExit("")
    if os.environ.get("NOTIFIER") is None:
        try:
            NOTIFIER = parser.get("settings", "NOTIFIER")
        except Exception as e:
            error("\nError: The config file could not be validated.\nPlease check that the file exists and is valid")
            raise SystemExit("")
    if BOT_TOKEN == "your_bot_token":
        error(
            "\nError: Sending failed. The Telegram token was not updated from its default value.\nPlease consult the README.md for more details"
        )
        exit()
    elif CHAT_ID == "your_chat_id":
        error(
            "\nError: Sending failed. The Telegram chat id was not updated from its default value.\nPlease consult the README.md for more details"
        )
        exit()
    if NOTIFIER != "telegram":
        error(
            "\nError: No valid notifier was specified. Please check your 'settings.ini' file"
        )
        exit()


def telegram(message, programs):
    default("\n\nsending message through telegram ...")
    programs_as_string = ""
    for i in programs:
        programs_as_string += i
        programs_as_string += "\n"
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    r = requests.post(
        url, data={"chat_id": CHAT_ID, "text": message + programs_as_string}
    )
    click.secho("message sent !", fg="green")


def notify(res, programs):
    prerequisites()
    if res is True:
        message = "✅ All the programs are up to date. \n"
    elif res is False:
        message = "⚠️ The following program(s) require an update: \n"
    telegram(message, programs)
