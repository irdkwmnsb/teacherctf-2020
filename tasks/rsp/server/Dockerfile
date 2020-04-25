FROM node:12

COPY app /app

WORKDIR /app

RUN npm install

RUN chmod +x entrypoint.sh

EXPOSE 3000

CMD ./entrypoint.sh