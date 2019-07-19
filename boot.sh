#!/bin/sh
source venv_for_web_dev/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - Hermes_Prediction:app