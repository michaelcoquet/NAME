# pull official base image
FROM alpine:latest


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3 python3-dev alpine-sdk libffi-dev musl-dev py3-pip py3-cryptography py3-pillow

# install dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install Pillow
RUN pip install --requirement ./requirements.txt
# copy project
COPY . .

EXPOSE 3000

ENTRYPOINT ["entrypoint.sh"]