# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable

# RUN apt-get install -y google-chrome-stable


# Use the official Python image.
FROM python:3.11-slim-bullseye

# Copy local code to the container image.
WORKDIR /app

# Install manually all the missing libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \   
    wget \
    unzip \    
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# copy code and assets from repo
COPY requirements.txt .

# Install Python dependencies.
RUN pip3 install -r requirements.txt

COPY main.py .

COPY .streamlit .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]