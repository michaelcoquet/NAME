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
RUN pip install --requirement ./requirements.txt
# copy project
COPY . .

ENTRYPOINT ["entrypoint.sh"]