# pull official base image
FROM python:3.9.6-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc python3-dev python3-pip cython3
RUN apt-get -y install python3-numpy python3-scipy apt-utils
RUN apt-get install -y gunicorn3 nginx
RUN apt install -y netcat

# install dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install Pillow
RUN pip install --requirement ./requirements.txt

# copy project
COPY . .

EXPOSE 8000
EXPOSE 443
EXPOSE 80

ENTRYPOINT ["./scripts/entrypoints/prod/main.sh"]