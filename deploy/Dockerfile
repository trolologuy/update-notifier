FROM ubuntu:20.04
LABEL name="update-notifier"

# install firefox and geckodriver
RUN apt-get update && apt-get upgrade -y && apt-get install firefox wget -y
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -xzf geckodriver-v0.26.0-linux64.tar.gz -C /usr/local/bin \
    && rm geckodriver-v0.26.0-linux64.tar.gz \
    && chmod +x /usr/local/bin/geckodriver \
    && export PATH=/usr/local/bin:$PATH 

# install the requirements and run the upgrade-notifier
COPY requirements.txt ~/home/requirements.txt
WORKDIR ~/home/
RUN apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    python3-lxml \
    python3-pip -y \
    && pip3 install -r requirements.txt

COPY . .
CMD python3 update-notifier.py -i installed.json