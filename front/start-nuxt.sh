#!/bin/bash
# Start frontend
echo "starting nuxt"
npm run build
pm2 logs > /dev/null 2>&1
IS_UP=$?
if [ $IS_UP -ne 0 ]; then
  pm2 start > /dev/null
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to start frontend ssr: $status" 1>&2
    exit $status
  fi
fi


COUNTER=0
MAX_ATTEMPTS=30

while [ $COUNTER -lt $MAX_ATTEMPTS ]; do
  IGNORE=$(timeout 1 bash -c 'cat < /dev/null > /dev/tcp/localhost/3002' 2> /dev/null)
  STATUS=$?
  if [ $STATUS == 0 ]
  then
    echo 'OK'
    exit 0
  else
    sleep 5
    COUNTER=$(( COUNTER + 1 ))
  fi
done

if [ $IS_UP -ne 0 ]; then
  pm2 delete 'iyb-app-ssr'
fi

echo "Exhausted $MAX_ATTEMPTS attempts, exiting with 1."
exit 1
