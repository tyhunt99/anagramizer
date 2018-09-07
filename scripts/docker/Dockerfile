FROM python:3.6.6

MAINTAINER Tyler Hunt "tyler.s.hunt05@gmail.com"

ADD build/app.tar /app/

ADD build/dictionary.tar /var/lib/anagramizer/

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]
