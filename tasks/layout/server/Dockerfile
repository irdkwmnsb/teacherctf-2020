FROM python:3.8

MAINTAINER @irdkwmnsb <me@alzhanov.ru>

WORKDIR /etc/layout

RUN mkdir /var/subway && \
    chown -R nobody:nogroup /var/subway

COPY ./requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY ./ ./

USER nobody:nogroup

CMD gunicorn --workers 4 --bind 0.0.0.0:8080 'layout:app'