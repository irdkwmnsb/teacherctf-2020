FROM python:3.9-bullseye

COPY bot /bot

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /bot

CMD ["python3", "bot.py"]