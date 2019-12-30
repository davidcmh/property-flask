FROM python:3.8-slim

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

ARG GOOGLE_API_KEY
ENV GOOGLE_API_KEY=$GOOGLE_API_KEY

COPY . /usr/src/app

CMD [ "gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "src.app:app" ]