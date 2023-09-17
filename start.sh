#!/bin/bash

set -uo pipefail

DIRNAME=$(dirname $0)


function include_or_die {
  printf "$1"
  RESULT=$($DIRNAME/$2 2>&1)
  if [ $RESULT != 'OK' ]
  then
    echo FAIL
    echo $RESULT 1>&2
    exit 1
  fi
  echo $RESULT
}


include_or_die "NUXT SPA Starting..." start-nuxt.sh
include_or_die "Django Starting..." run_web.sh