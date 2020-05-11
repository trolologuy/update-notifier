#!/usr/bin/python3
"""
Update Notifier script v0.1
The purpose of this script is to parse 
a JSON file and check if the version of the software stated in it 
is the latest available.
If not, a telegram notification is sent.
"""

import os
import sys
import json
import getopt
import requests
from notifier import notify
from bs4 import BeautifulSoup
from configparser import ConfigParser

parser = ConfigParser()
parser.read('settings.ini')

BOT_TOKEN = parser.get('telegram', 'BOT_TOKEN')
CHAT_ID = parser.get('telegram', 'CHAT_ID')

def check_prerequisites():
    """Makes sure Python 3 is used"""
    if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
        print("Error: this script requires Python 3.6 or higher")
        print(
            "You are using Python {}.{}.".format(
                sys.version_info.major, sys.version_info.minor
            )
        )
        print("you can try with command: python3 ./clip.py")
        sys.exit(2)

def get_arg(argv):
    """Get the command line arguments"""
    check_prerequisites()

    inputfile = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print("Error: Missing argument --> main.py -i <JSON file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("clip.py -i <JSON file>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    if "." not in inputfile:
        print("Error: Missing the file extension for the JSON file passed as argument --> main.py -i <JSON file>")
        sys.exit(2)

    # check if both files exist
    if not os.path.isfile(inputfile):
        print("Error: the input file", inputfile, "does not exist")
        sys.exit(2)

    main(inputfile)

def get_json_from_url(url):
    response = requests.get(url)
    return(response)

def plex():
    """Returns the latest Plex version available for plex."""
    # curl -sq https://plex.tv/api/downloads/5.json | jq .nas.Synology.version
    data = get_json_from_url("https://plex.tv/api/downloads/5.json")
    return(data.json())


def main(inputfile):
    """The main function"""
    programs = []
    res = 0
    with open(inputfile) as f:
        data = json.load(f)
    if plex()["nas"]["Synology"]["version"] == data["storage"]["nas"]["synology"]:
        print("plex is up to date")
    else:
        print("plex is not up to date")
        print("Latest version available is: " + plex()["nas"]["Synology"]["version"])
        print("You are using: "+ data["storage"]["nas"]["synology"] + '\n')
        res = 1
        programs.append("Plex")
    notify(res, programs)

if __name__ == "__main__":
    get_arg(sys.argv[1:])