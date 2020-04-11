FROM python:latest

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app .

EXPOSE 8888

ENV FLASK_APP app.py

ENTRYPOINT [ "flask" ]
CMD [ "run", "-h", "0.0.0.0", "-p", "8888", "--with-threads" ]
