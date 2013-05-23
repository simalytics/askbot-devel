#!/bin/sh
ssh -i askbot-test-ec2.pem -L 9312:localhost:9312 ubuntu@ec2-50-16-150-32.compute-1.amazonaws.com &
newrelic-admin run-program python manage.py run_gunicorn "0.0.0.0:$PORT" -w 3

