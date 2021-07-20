# pull official base image
FROM python:3.9.6-buster


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc python3-dev python3-pip cython3
RUN apt-get -y install python3-numpy python3-scipy apt-utils
RUN apt-get install -y rabbitmq-server
RUN apt install -y netcat

# install dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install Pillow
RUN pip install --requirement ./requirements.txt
# RUN rabbitmq-plugins enable --offline rabbitmq_management
# copy project
COPY . .

ENTRYPOINT ["entrypoint.sh"]