FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir /jobnet
WORKDIR /jobnet

RUN pip install --upgrade pip
COPY requirements.txt /jobnet/
RUN pip install -r requirements.txt

COPY . /jobnet/