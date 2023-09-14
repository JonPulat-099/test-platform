#!/bin/sh
python3 manage.py makemigrations
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to makemigrations: $status"
  exit $status
fi
echo "makemigrations ->  OK"

python3 manage.py migrate
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to migrate: $status"
  exit $status
fi
echo "migrate ->  OK"

python3 manage.py shell < add_user.py
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to add user: $status"
  exit $status
fi
echo "add user ->  OK"

python3 manage.py runserver 0.0.0.0:8000
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to runserver: $status"
  exit $status
fi
echo "runserver ->  OK"
