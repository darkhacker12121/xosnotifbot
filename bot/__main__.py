#!/usr/bin/env python3
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

import logging
# Python imports
import os
import sys

# Library imports
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler

# Project imports
from bot import commands, custom_filters

argv_len = len(sys.argv) - 1

if argv_len < 1 and "NOLIFER_TG_TOKEN" not in os.environ:
    print("Please specify your token or export it as NOLIFER_TG_TOKEN")
    exit(1)

bot_token = os.environ['NOLIFER_TG_TOKEN'] if argv_len < 1 else sys.argv[1]
bot_instance = 1
bot_dir = os.path.dirname(os.path.abspath(__file__))

webhook_url_path = "%s-%i" % (bot_token, bot_instance)
webhook_port = int(os.environ['NOLIFER_WEBHOOK_PORT']) \
    if "NOLIFER_WEBHOOK_PORT" in os.environ \
    else 24627
webhook_listen = os.environ['NOLIFER_WEBHOOK_LISTEN'] \
    if "NOLIFER_WEBHOOK_LISTEN" in os.environ \
    else '127.0.0.1'
webhook_url = "https://%s/%s" % (os.environ['NOLIFER_WEBHOOK_BASEURL']
                                 if "NOLIFER_WEBHOOK_BASEURL" in os.environ
                                 else webhook_listen, webhook_url_path)

def start_bot():
    print("Starting bot located at %s" % bot_dir)
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    try:
        bot = telegram.Bot(token=bot_token)
        print("Token approved, proceeding with initialization")
    except telegram.error.InvalidToken:
        print("Error: invalid token '%s'. "
              "Make sure your Telegram bot token is correct"
              % bot_token)
        exit(1)
    print("This is %s" % bot.get_me()['first_name'])
    print("Initializing updater...")
    try:
        updater = Updater(token=bot_token)
        print("  Listen: %s\n"
              "  Port:   %i\n"
              "  URL:    %s" % (webhook_listen, webhook_port, webhook_url))
        updater.start_webhook(listen=webhook_listen,
                              port=webhook_port,
                              url_path=webhook_url_path)
        updater.bot.set_webhook(url=webhook_url,
                                certificate=open(
                                    "%s/../cruft/cert.pem" % bot_dir, "rb"))
        dispatcher = updater.dispatcher
    except Exception as e:
        print("Error while initializing updater: %s" % e)
        exit(1)
    print("Updater successfully set up.")
    print("Checking for recent restart...")
    try:
        with open("/tmp/nolifer-stop-reason", "r") as tmpfile:
            filecont = tmpfile.readline().strip().split()
        reason = filecont[0]
        chat_id = filecont[1]
        if reason == "restart":
            bot.sendMessage(chat_id=chat_id,
                            text="Restart successful.")
        os.remove("/tmp/nolifer-stop-reason")
    except:
        # Don't bother
        print("Not bothering about stop reason")

    print("Setting up handlers...")
    for command in commands.commands:
        dispatcher.add_handler(CommandHandler(command[0], command[1]))
    for filter_ in custom_filters.filters:
        dispatcher.add_handler(MessageHandler(filter_[0], filter_[1]))
    print("Listening.")
    updater.idle()
    print("Stopped")

if __name__ == "__main__":
    if argv_len > 0 and sys.argv[1] == "sanity-check":
        print("success")
        exit(0)
    else:
        start_bot()
