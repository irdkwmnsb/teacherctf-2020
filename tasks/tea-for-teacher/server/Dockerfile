FROM python:3.7-alpine

COPY app /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /app

EXPOSE 9999

CMD ["gunicorn", "--workers=2", "--threads=4", "-b",  "0.0.0.0:80", "sourcefile:app"]
