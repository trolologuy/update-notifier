#!/usr/bin/python3
# pylint: disable=line-too-long
"""
The purpose of this file is to handle notifications.
It reads a "settings.ini" file.
"""

import os
import sys
from configparser import ConfigParser
import click
import requests

PARSER = ConfigParser()
try:
    PARSER.read("settings.ini")
except Exception as error_message:
    error(
        "Error: The config file could not be validated.\nPlease check that the file exists and is valid"
    )
    default(error_message)
    raise SystemExit("")


def default(message):
    """Default message used as an alternative to print()"""
    click.secho(message, fg="white")


def warning(message):
    """Default warning message used as an alternative to print()"""
    click.secho(message, fg="blue", blink=True, bold=True)


def error(message):
    """Default error message used as an alternative to print()"""
    click.secho(message, fg="red")


def env_checker(token, section):
    """
    Checks if the variable are set in the env,
    if not, the settings file is being read and the values are extracted and set
    """
    if os.environ.get(token):
        return os.environ.get(token)
    elif os.environ.get(token) is None:
        try:
            if token == "BOT_TOKEN":
                return PARSER.get(section, token)
            elif token == "CHAT_ID":
                return PARSER.get(section, token)
            elif token == "NOTIFIER":
                return PARSER.get(section, token)
            else:
                return None
        except Exception as error_message:
            error(
                "\nError: The config file could not be validated.\nPlease check that the file exists and is valid"
            )
            default(error_message)
            raise SystemExit("")
    else:
        return None


def check_default(bot_token, chat_id, notifier):
    """Checks if the default value from the settings.ini have been changed"""
    error_start = "\nError: Sending failed. The"
    error_end = "was not updated from its default value.\nPlease consult the README.md for more details"
    if bot_token == "your_bot_token":
        error(error_start + " telegram token " + error_end)
        sys.exit()
    elif chat_id == "your_chat_id":
        error(error_start + " telegram chat ID " + error_end)
        sys.exit()
    if notifier != "telegram":
        error(
            "\nError: No valid notifier was specified. Please check your 'settings.ini' file"
        )
        sys.exit()


def prerequisites():
    """
    Checks the prerequisites for the programm to work
    Basically it checks that the values are set (parses env and config file)
    and that the default values have been changed
    """
    global BOT_TOKEN
    global CHAT_ID

    BOT_TOKEN = env_checker("BOT_TOKEN", "telegram")
    CHAT_ID = env_checker("CHAT_ID", "telegram")
    notifier = env_checker("NOTIFIER", "settings")

    check_default(BOT_TOKEN, CHAT_ID, notifier)


def telegram(message, programs):
    """
    The function that allows to send through telegram
    """
    default("\n\nsending message through telegram ...")
    programs_as_string = ""
    for i in programs:
        programs_as_string += i
        programs_as_string += "\n"
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message + programs_as_string})
    click.secho("message sent !", fg="green")


def notify(res, programs):
    """
    The main function
    """
    prerequisites()
    if res is True:
        message = "✅ All the programs are up to date. \n"
    elif res is False:
        message = "⚠️ The following program(s) require an update: \n"
    telegram(message, programs)
