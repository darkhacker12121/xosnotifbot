#!/bin/bash

echo "This script will download all necessary files and set up this bot" \
     "for immediate use. Make sure you have an active internet connection."

which curl 2>&1 >/dev/null
if [ $? -eq 0 ]; then
  echo "  Doing connectivity check..."
  curl http://connectivitycheck.gstatic.com/generate_204
  if [ $? -ne 0 ]; then
    echo "  Connectivity check failed! Use a working internet connection."
    exit 1
  else
    echo "  Connectivity check successful."
  fi
fi

echo "Starting setup..."
cd bot
./fetch-and-setup.sh

exit $?
