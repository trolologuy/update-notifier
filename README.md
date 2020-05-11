# update-notifier
<a href="https://github.com/trolologuy/update-notifier/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Notifies you when updates for the selected software is available.
Only supports telegram bot notification for now.

## Prerequisites
- Having Python 3 installed

## Installation
1. Run the following command to install the required modules locally
   `pip3 install -U -r requirements.txt --user`
2. Rename the `settings.example.ini` to `settings.ini`
3. Edit the `settings.ini` and add your credentials.
4. Edit the `installed.json` and add the value of the __exact__ version of the software you are currently using __Warning: Currently only Plex is supported__

## Usage
`python3 main.py -i installed.json`

### Telegram
If you need help getting the `BOT_TOKEN` and `CHAT_ID` variables, please follow the *steps 1* and *2* in this [gist](https://gist.github.com/trolologuy/c290ac3edc46fe6bc2b69ccc497cd4bc)

# Similar project
[nvchecker](https://github.com/lilydjwg/nvchecker)

## TO DO
- [x] add .ini file parsing
- [x] add telegram support
- [ ] add download link to the latest version of the software (to be added in the `installed.json`)
- [ ] add better error handling
- [ ] add testing
- [ ] add CI / CD
- [ ] add installation as a package
- [ ] add more options for the `installed.json` file
- [ ] add other possibilities for the notifications