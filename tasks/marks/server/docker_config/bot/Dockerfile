FROM python:3.9-alpine

# Check available versions here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
ARG CHROME_VERSION="81.0.4044.138-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

COPY bot /bot

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /bot

CMD ["python3", "bot.py"]