FROM python:3.8-slim-buster

# Do not cache Python packages
ENV PIP_NO_CACHE_DIR=yes

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# set PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/code/"

# Initializing new working directory
WORKDIR /code

# Transferring the code and essential data
COPY xetra ./xetra
COPY requirements.txt ./requirements.txt
COPY main.py ./main.py

RUN pip install -r ./requirements.txt