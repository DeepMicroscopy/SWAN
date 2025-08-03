FROM python:3.13.5-alpine3.22

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apk add --no-cache libmagic
RUN addgroup swan && adduser -h /app/ -s /bin/sh -G swan -D swan

USER swan
WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000/tcp
VOLUME /media/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:5000" ]