#!/bin/sh
ssh -o StrictHostKeyChecking=no -i askbot-test-ec2.pem -L 9312:localhost:9312 ubuntu@107.21.228.25 &&
newrelic-admin run-program python manage.py run_gunicorn "0.0.0.0:$PORT" -w 3

