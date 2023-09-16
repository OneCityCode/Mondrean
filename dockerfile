# Use the official Python image.
FROM python:3.11-slim-bullseye

# Install all the missing libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \   
    wget

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# create folder for app
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#copy app code
COPY main.py .
COPY .streamlit .

# expose and check port
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# starts app
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]