# update-notifier
<a href="https://github.com/trolologuy/update-notifier/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Notifies you when updates for the selected software is available.

[![asciicast](https://asciinema.org/a/330224.svg)](https://asciinema.org/a/330224)

### Features
- Bot Telegram notifications :robot:
- Easy deploy through __Vagrant__ or __Docker__ ! 
- Supports the following websites / services :
   - [Plex](https://www.plex.tv/) → Only the [Synology NAS version](https://www.plex.tv/media-server-downloads/) for now.
   - [Synology DSM version](https://www.synology.com/en-us/dsm) → [Downloads page](https://www.synology.com/en-us/support/download)
   - [pfsense](https://www.netgate.com/solutions/pfsense/features.html) → [Downloads page](https://www.pfsense.org/download/)
   - [Unifi cloud key](https://www.ui.com/unifi/unifi-cloud-key/) → [Downloads page](https://www.ui.com/download/unifi/unifi-cloud-key)
   - [Wordpress](https://wordpress.org/) → [Downloads page](https://wordpress.org/download/)
- Easy integration as cronjob. If you want to monitor the cronjob, you can use [healthchecks](healthchecks.io/).

## Prerequisites
- Having Python 3 installed
- Having [geckodriver](https://github.com/mozilla/geckodriver/releases/) installed in `/usr/local/bin/geckodriver`(or edit the path in the `SELENIUM` variable in the `settings.ini` file)

## Installation
1. Rename the `settings.example.ini` to `settings.ini`
2. Edit the `settings.ini` and add your credentials (more explanation regarding the variables below).
3. Edit the `installed.json` and add the value of the __exact__ version of the software you are currently using.
4. Run the following command to install the required modules locally `pip3 install -U -r requirements.txt --user`

You could run this project in docker with a cronjob, so that the update checks are run once a day or once a week for example.

### Usage
`python3 update-notifier.py -i installed.json`


## Configuration file (settings.ini)
### [settings]
- `NOTIFIER` by default `telegram` since currently nothing else is supported.
- `SELENIUM` by default `/usr/local/bin/geckodriver` since that's where I decided to install it for docker and vagrant. If you install *geckodriver* manually you may have to adapt this path.
- `HEALTHCHECK`by default a random non-valid url. This is an URL that is to be pinged when the script was succesfully run. If you want to monitor the cronjob(s), you can use [healthchecks](healthchecks.io/).

### [telegram]
- `BOT_TOKEN` Please update this Token accordingly (more details below).
- `CHAT_ID` Please update this ID accordingly (more details below).
If you need help getting the `BOT_TOKEN` and `CHAT_ID` variables, please follow the *steps 1 and *2* in this [gist](https://gist.github.com/trolologuy/c290ac3edc46fe6bc2b69ccc497cd4bc)


## Deployment

You can also deploy the project through docker or vagrant.

### Docker
1. Install Docker
2. Run either `docker-compose up` or `docker build -t update-notifier -f deploy/Dockerfile .` and `docker run --rm -d --name notify update-notifier` if you want to use the Dockerfile directly. We are using the parameter `--rm` to auto-delete the container once it has sent the notification.

__Important Note__: Since the content of the repo is copied into the container, everytime you modify one of the files you will have to rebuild the image and start a container using that freshly built image.

### Vagrant
1. Install Vagrant
2. Install virtualbox
3. `cd deploy/vagrant` to access the right folder
4. `vagrant up` to start the virtual machine and the script

To destroy your Vagrant image:
`vagrant destroy --force`


If you encounter any issue with the setting up of the project, feel free to open an issue :) 


# Similar projects
* [anitya](https://github.com/fedora-infra/anitya)
* [nvchecker](https://github.com/lilydjwg/nvchecker)