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
import click
import getopt
import progress
import requests
import regex as re
from progress.bar import IncrementalBar
from bs4 import BeautifulSoup
from selenium import webdriver
from configparser import ConfigParser
from notifier import notify

parser = ConfigParser()
try:
    parser.read("settings.ini")
except Exception as e:
    error("Error: The config file could not be validated.\nPlease check that the file exists and is valid")
    raise SystemExit("")

PFSENSE = "Pfsense"
PLEX = "Plex"
SYNOLOGY_DSM = "Synology DSM"
UNIFI_CC = "Unifi Cloud Key Controller"
WORDPRESS = "Wordpress"

def default(message):
    click.secho(message, fg='white')

def warning(message):
    click.secho(message, fg='blue', blink=True, bold=True)

def error(message):
    click.secho(message, fg='red')

def prerequisites():
    """Makes sure Python 3 is used and the default values have been updated"""
    global HEALTHCHECK
    global SELENIUM
    HEALTHCHECK = os.environ.get("HEALTHCHECK")
    SELENIUM = os.environ.get("SELENIUM")

    if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
        error("Error: this script requires Python 3.6 or higher")
        error(
            "You are using Python {}.{}.".format(
                sys.version_info.major, sys.version_info.minor
            )
        )
        default("Please use: python3 ./main.py")
        sys.exit(2)
    default("Reading settings.ini ...")
    if os.environ.get("HEALTHCHECK") is None:
        try:
            HEALTHCHECK = parser.get("settings", "HEALTHCHECK")
        except Exception as e:
            error("Error: The config file could not be validated.\nPlease check that the file exists and is valid")
            raise SystemExit("")
    if os.environ.get("SELENIUM") is None:
        try:
            SELENIUM = parser.get("settings", "SELENIUM")
        except Exception as e:
            error("Error: The config file could not be validated.\nPlease check that the file exists and is valid")
            raise SystemExit("")
    if HEALTHCHECK == "https://some-domain.com/and_some_token":
        warning(
            "The Healthchecks url was not updated from its default value.\n"
        )
    if SELENIUM == "/usr/local/bin/geckodriver":
        warning(
            "Using the default location for the geckodriver: '/usr/local/bin/geckodriver'.\nYou can change this setting under 'SELENIUM' in the 'settings.ini' file."
        )

def get_arg(argv):
    """Get the command line arguments"""
    prerequisites()

    inputfile = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print("Error: Missing argument.\nUsage: main.py -i <JSON file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("clip.py -i <JSON file>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    if "." not in inputfile:
        error(
            "Error: Missing the file extension for the JSON file passed as argument.\nUsage: main.py -i <JSON file>"
        )
        sys.exit(2)

    # check if both files exist
    if not os.path.isfile(inputfile):
        error("Error: the input file", inputfile, "does not exist")
        sys.exit(2)

    main(inputfile)


def get_json_from_url(url):
    response = requests.get(url)
    return response


def create_headless_firefox_browser():
    """Creates a headless Firefox browser."""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(executable_path=SELENIUM, options=options)


def check_numbers_or_dots(to_clean):
    expression = r"([0-9].[0-9]*.[0-9]*)/"
    result = re.search(expression, to_clean)
    if result:
        return result.group(1)
    return None


def pfsense():
    """Returns the latest version available for pfsense."""
    expression = r"<p> (.*) <\/p>"
    page = requests.get("https://www.pfsense.org/download/")
    soup = BeautifulSoup(page.text, "html.parser")
    list = soup.find(class_="col-sm-9")
    match = str(list.find("p"))
    result = re.search(expression, match)

    if result:
        return result.group(1)
    else:
        print(
            "Error: The current version of the unifi cloudkey controller could not be retrieved !"
        )
        return None


def synology_dsm():
    """Returns the latest version available for DSM on synology."""
    expression = r"<p> (.*) <\/p>"
    result = []
    page = requests.get("https://archive.synology.com/download/DSM/release/")
    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all("a"):
        tmp = check_numbers_or_dots(link.get("href"))
        if tmp is not None:
            result.append(tmp)
    return sorted(result, key=None, reverse=True)[0]


def synology_plex():
    """Returns the latest version available for plex on synology."""
    data = get_json_from_url("https://plex.tv/api/downloads/5.json")
    return data.json()


def unifi():
    """Returns the latest version available for unifi products."""
    expression = r"UniFi Cloud Key firmware (.*)<\/td>"

    browser = create_headless_firefox_browser()
    cloud_key_url = "https://www.ui.com/download/unifi/unifi-cloud-key"
    browser.get(cloud_key_url)
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    # Result is similar to:
    # <td class="downloadResults__name">UniFi Cloud Key firmware 1.1.11</td>
    match = str(soup.find("td", attrs={"class": "downloadResults__name"}))
    result = re.search(expression, match)

    if result:
        return result.group(1)
    else:
        error(
            "Error: The current version of the unifi cloudkey controller could not be retrieved !"
        )
        return None


def wordpress():
    """Returns the latest version available for wordpress."""
    data = get_json_from_url("https://api.wordpress.org/core/version-check/1.7/")
    return data.json()


def message(service, up_to_date, latest, installed):
    if up_to_date is True:
        click.echo(
            " - "
            + click.style(service, fg="yellow")
            + click.style(" is up to date.", fg="green")
        )
    elif up_to_date is False:
        click.echo(
            " - "
            + click.style(service, fg="yellow")
            + click.style(" is not up to date.", fg="red")
        )
        click.echo("   Latest version available is: " + click.style(latest, fg="blue"))
        click.echo("   You are using:: " + click.style(installed, fg="cyan"))


def main(inputfile):
    """The main function"""
    programs = []
    up_to_date = True
    click.echo(
        click.style(
            """
+---------------------------------------------------------------------------------------------------------+
|                           _                                              _   ___  _                     |
|                          | |        _                              _    (_) / __)(_)                    |
|         _   _  ____    _ | |  ____ | |_   ____  ___  ____    ___  | |_   _ | |__  _   ____   ____       |
|        | | | ||  _ \  / || | / _  ||  _) / _  )(___)|  _ \  / _ \ |  _) | ||  __)| | / _  ) / ___)      |
|        | |_| || | | |( (_| |( ( | || |__( (/ /      | | | || |_| || |__ | || |   | |( (/ / | |          |
|         \____|| ||_/  \____| \_||_| \___)\____)     |_| |_| \___/  \___)|_||_|   |_| \____)|_|          |
|             |_|                                                                                         |
+---------------------------------------------------------------------------------------------------------+
   """,
            fg="yellow",
        )
    )
    default("Gathering informations...\n")
    with open(inputfile) as f:
        data = json.load(f)

    # Progressbar
    bar = IncrementalBar("Processing", max=5)
    for i in range(1):
        latest_pfsense_version = pfsense()
        bar.next()
        latest_synology_dsm_version = synology_dsm()
        bar.next()
        latest_synology_plex_version = synology_plex()["nas"]["Synology"]["version"]
        bar.next()
        latest_unifi_ck_version = unifi()
        bar.next()
        latest_wordpress_version = wordpress()["offers"][0]["current"]
        bar.next()
        bar.finish()
    default("\n")
    installed_pfsense_version = data["networking"]["firewall"]["pfsense"]
    installed_synology_dsm_version = data["storage"]["nas"]["synology"]["dsm"]
    installed_synology_plex_version = data["storage"]["nas"]["synology"]["plex"]
    installed_unifi_ck_version = data["networking"]["unifi"]["cloudkey"]
    installed_wordpress_version = data["hosting"]["cms"]["wordpress"]

    if latest_synology_dsm_version == installed_synology_dsm_version:
        message(SYNOLOGY_DSM, True, "", "")
    else:
        message(
            SYNOLOGY_DSM,
            False,
            latest_synology_dsm_version,
            installed_synology_dsm_version,
        )
        up_to_date = False
        programs.append(SYNOLOGY_DSM)
    if latest_synology_plex_version == installed_synology_plex_version:
        message(PLEX, True, "", "")
    else:
        message(
            PLEX, False, latest_synology_plex_version, installed_synology_plex_version
        )
        up_to_date = False
        programs.append(PLEX)
    if latest_unifi_ck_version == installed_unifi_ck_version:
        message(UNIFI_CC, True, "", "")
    else:
        message(UNIFI_CC, False, latest_unifi_ck_version, installed_unifi_ck_version)
        up_to_date = False
        programs.append(UNIFI_CC)
    if latest_wordpress_version == installed_wordpress_version:
        message(WORDPRESS, True, "", "")
    else:
        message(WORDPRESS, False, latest_wordpress_version, installed_wordpress_version)
        up_to_date = False
        programs.append(WORDPRESS)
    if latest_pfsense_version == installed_pfsense_version:
        message(PFSENSE, True, "", "")
    else:
        message(PFSENSE, False, latest_pfsense_version, installed_pfsense_version)
        up_to_date = False
        programs.append(PFSENSE)

    notify(up_to_date, programs)

    # Used for the Healtchecks ping, if it's not used, it fails silently.
    try:
        requests.get(HEALTHCHECK)
        print("The Healthchecks Ping URL was succesfully contacted.")
    except requests.exceptions.RequestException as e:
        raise SystemExit("")


if __name__ == "__main__":
    get_arg(sys.argv[1:])
