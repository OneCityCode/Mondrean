FROM python:3.11-slim-bullseye

# # Copy local code to the container image.
# WORKDIR /app

# # copy code and assets from repo
# COPY . .

# # Install manually all the missing libraries
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     wget     
#     #&& rm -rf /var/lib/apt/lists/*

# # Install Chrome
# #RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# #RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable

# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # set display port to avoid crash
# ENV DISPLAY=:99

# # Install Python dependencies.
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# EXPOSE 8501

# #HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
   mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
   curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
   unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
   rm /tmp/chromedriver_linux64.zip && \
   chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
   ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o – https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add – && \
   echo “deb http://dl.google.com/linux/chrome/deb/ stable main” >> /etc/apt/sources.list.d/google-chrome.list && \
   apt-get -yqq update && \
   apt-get -yqq install google-chrome-stable && \
   rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
  unzip \
  curl \
  gnupg \
  && rm -rf /var/lib/apt/lists/*
  
RUN curl -sS -o – https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add

RUN echo “deb http://dl.google.com/linux/chrome/deb/ stable main” >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .

CMD [ “python”, “scrap.py” ]