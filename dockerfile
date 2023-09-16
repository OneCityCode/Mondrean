# # Use the official Python image.
# FROM python:3.11-slim-bullseye

# # Copy local code to the container image.
# WORKDIR /app

# # Install manually all the missing libraries
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \   
#     wget \
#     unzip \    
#     && rm -rf /var/lib/apt/lists/*

# # Install Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# # copy code and assets from repo
# COPY requirements.txt .

# # Install Python dependencies.
# RUN pip3 install -r requirements.txt

# COPY main.py .

# COPY .streamlit .

# EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

FROM python:3.11-slim-bullseye

USER root

# Install manually all the missing libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \   
    wget \
    unzip \    
    && rm -rf /var/lib/apt/lists/*

# Google Chrome
ARG CHROME_VERSION="google-chrome-stable"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install \
    ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Chrome Launch Script Wrapper
COPY wrap_chrome_binary /opt/bin/wrap_chrome_binary
RUN /opt/bin/wrap_chrome_binary

USER 1200

# Chrome webdriver
ARG CHROME_DRIVER_VERSION
RUN if [ ! -z "$CHROME_DRIVER_VERSION" ]; \
  then CHROME_DRIVER_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip ; \
  else echo "Geting ChromeDriver binary from https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
    && CFT_URL=https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json \
    && CFT_CHANNEL="Stable" \
    && if [ "$CHROME_VERSION" = "google-chrome-beta" ]; then CFT_CHANNEL="Beta" ; fi \
    && if [ "$CHROME_VERSION" = "google-chrome-unstable" ]; then CFT_CHANNEL="Dev" ; fi \
    && echo $CFT_CHANNEL \
    && CTF_VALUES=$(curl -sSL $CFT_URL | jq -r --arg CFT_CHANNEL "$CFT_CHANNEL" '.channels[] | select (.channel==$CFT_CHANNEL)') \
    && CHROME_DRIVER_VERSION=$(echo $CTF_VALUES | jq -r '.version' ) \
    && CHROME_DRIVER_URL=$(echo $CTF_VALUES | jq -r '.downloads.chromedriver[] | select(.platform=="linux64") | .url' ) ; \
  fi \
  && echo "Using ChromeDriver from: "$CHROME_DRIVER_URL \
  && echo "Using ChromeDriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip $CHROME_DRIVER_URL \
  && rm -rf /opt/selenium/chromedriver \
  && sudo unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && sudo mv /opt/selenium/chromedriver-linux64/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && sudo chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && sudo ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver

# Dumping Browser name and version for config
RUN echo "chrome" > /opt/selenium/browser_name

WORKDIR /app

# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .

COPY .streamlit .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
