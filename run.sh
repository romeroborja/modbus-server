#! /bin/bash
action=$1
slect=$2

trap "exit_apps" 2

function exit_apps () {
  echo -e "\nCLOSING APPLICATION.\n"
  docker compose stop
  exit 0
}

if [ ! -z $action ]
then

  if [ $action = -e ]
  then
    if [[ $slect == "dev" ]]
    then
      echo -e "\nRUNNING THE APPLICATION IN DEVELOPMENT MODE.\n"
      docker compose -f docker-compose-dev.yml up
    elif [[ $slect == "prod" ]]
    then
      echo -e "\nRUNNING THE APPLICATION IN PRODUCTION MODE.\n"
      docker compose -f docker-compose-prod.yml up
    fi
  fi
else
  echo "You must enter input parameters"
fi
