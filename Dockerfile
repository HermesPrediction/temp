FROM python:3.6-alpine

RUN adduser -D Hermes_Prediction

WORKDIR /home/Hermes_Prediction

COPY requirements.txt requirements.txt
RUN python -m venv venv_for_web_dev
RUN venv_for_web_dev/bin/pip install -r requirements.txt
RUN venv_for_web_dev/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY Hermes_Prediction.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP Hermes_Prediction.py

RUN chown -R Hermes_Prediction:Hermes_Prediction ./
USER Hermes_Prediction

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]