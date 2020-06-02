FROM python:3.8.1-slim-buster

ENV HOME_DIR=/var/FishPond
ADD . ${HOME_DIR}

WORKDIR ${HOME_DIR}

RUN pip3 install -r ${HOME_DIR}/server/requirements.txt

