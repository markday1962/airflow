#!/bin/sh
CMD_AIRFLOW_PASSED_COMMAND="$1"

case ${CMD_AIRFLOW_PASSED_COMMAND} in
  webserver)
    airflow initdb
    exec airflow webserver
    ;;
  scheduler)
    exec airflow scheduler
    ;;
  *)
    exec "@"
    ;;
esac
