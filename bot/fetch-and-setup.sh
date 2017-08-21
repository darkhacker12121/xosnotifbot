#!/bin/bash

echo
echo "Cloning python telegram bot API repository"
git clone https://github.com/python-telegram-bot/python-telegram-bot.git
echo "Preparing python telegram bot setup"
cd python-telegram-bot
if [ "$(whoami)" != "root" ]; then
  echo "  Root access is required to install necessary dependencies."
  read -p "  Do you want to grant root permission? [y/N]: " -n 1 -r
  [[ ! $REPLY =~ ^[Yy]$ ]] && echo -e "\nAborted." && exit 1
  echo
  echo "    Trying to gain root permission..."
  if [ "$(sudo whoami)" == "root" ]; then
    echo "    -> Success!"
  else
    echo "    -> Failed!"
    exit 1
  fi
fi
echo "Installing"
sudo python setup.py install
cd ..
echo "Symlinking telegram module"
ln -sf python-telegram-bot/telegram telegram
echo "Generating SSL certificate"
cd ..
mkdir -p cruft
cd cruft
openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
echo "  SSL certificate is valid for 10 years from now."
cd ../bot
echo "Doing sanity check"
result_ns="$(./nolifer.py sanity-check)"
if [ $? -ne 0 ] || [ "$result_ns" != "success" ]; then
  echo "  Sanity check failed, please make sure python is working properly"
  echo "  and that the script 'nolifer.py' is executable. Exiting now."
  exit 1
fi
echo "Done. Start the bot using this command:"
echo "  ./nolifer <telegram bot token>"
echo
echo "Set the environment variable NOLIFER_TG_TOKEN if you don't want to" \
     "pass it as environment variable"
echo "Set the environment variable NOLIFER_WEBHOOK_LISTEN to the IP you want" \
     "to listen to, defaults to 127.0.0.1 if not set"
echo "Set the environment variable NOLIFER_WEBHOOK_BASEURL to the domain or" \
     "IP of your server e. g. telegram.yourbot.com, defaults to listen address"
echo "Set the environment variable NOLIFER_WEBHOOK_PORT to the port you want" \
     "to listen to. You have to use a reverse proxy if you want to use a" \
     "different port than 80, 88, 443 or 8443. Defaults to 24627 if not set"
echo