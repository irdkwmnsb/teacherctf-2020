FROM python:3.7-alpine

COPY marks /marks

COPY marks/static /static

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /marks

RUN touch db.sqlite3

RUN python3 manage.py makemigrations && python3 manage.py migrate

EXPOSE 8000 

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "--threads=4", "marks.wsgi"]
