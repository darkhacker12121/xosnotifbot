#!/bin/bash
#
# Telegram Bot written in Python for halogenOS
# Copyright (C) 2017  Simao Gomes Viana
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

fallback_install() {
  echo "You might need to install dependencies manually"
  echo
  echo "Cloning python telegram bot API repository"
  git clone https://github.com/python-telegram-bot/python-telegram-bot.git \
      --recursive
  echo "Preparing python telegram bot setup"
  cd python-telegram-bot
  echo "Installing"
  sudo python setup.py install
  cd ..
  echo "Symlinking telegram module"
  ln -sf python-telegram-bot/telegram telegram
  cd ..
}

echo
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
which pip3 2>/dev/null >/dev/null
if [ $? -ne 0 ]; then
  echo "pip3 not installed, falling back to github fetch."
  fallback_install
else
  if [ 0$(pip3 --version | cut -d ' ' -f2 | cut -d '.' -f1) -lt 9 ]; then
    echo "pip3 version not 9+, falling back to github fetch."
    fallback_install
  else
    rm -rf python-telegram-bot
    rm -f telegram
    rm -f *.pyc
    sudo pip3 install python-telegram-bot --upgrade
    cd ..
  fi
fi
if [ -f "cruft/cert.pem" ] && [ -f "cruft/private.key" ]; then
  echo "SSL certificate already exists, not generating a new one."
else
  echo "Generating SSL certificate"
  mkdir -p cruft
  cd cruft
  openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
  echo "  SSL certificate is valid for 10 years from now."
  cd ..
fi
cd bot
echo "Doing sanity check"
result_ns="$(python3 -m bot sanity-check)"
if [ $? -ne 0 ] || [ "$result_ns" != "success" ]; then
  echo "  Sanity check failed, please make sure python is working properly"
  echo "  and that everything in bot/ is accessible. Also make sure all "
  echo "  dependencies are properly installed. Exiting now."
  exit 1
fi
echo "Done. In the bot directory start the bot using this command:"
echo "  python3 -m bot <telegram bot token>"
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