#!/usr/bin/env python

# Python imports
import os
import sys

# Library imports
import telegram
from telegram.ext import Updater, CommandHandler
import logging

# Project imports
import commands

argv_len = len(sys.argv) - 1

if argv_len < 1 and not "NOLIFER_TG_TOKEN" in os.environ:
  print("Please specify your token or export it as NOLIFER_TG_TOKEN")
  exit(1)

bot_token = os.environ['NOLIFER_TG_TOKEN'] if argv_len < 1 else sys.argv[1]
bot_dir = os.path.dirname(os.path.abspath(__file__))
bot = None
updater = None
dispatcher = None
webhook_url_path = "NOLIFER"
webhook_port = int(os.environ['NOLIFER_WEBHOOK_PORT']) \
                if "NOLIFER_WEBHOOK_PORT" in os.environ \
                else 24627
webhook_listen = os.environ['NOLIFER_WEBHOOK_LISTEN'] \
                  if "NOLIFER_WEBHOOK_LISTEN" in os.environ \
                  else '127.0.0.1'
webhook_url = "https://%s/%s" % \
                (os.environ['NOLIFER_WEBHOOK_BASEURL'] \
                  if "NOLIFER_WEBHOOK_BASEURL" in os.environ \
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
  update_queue = None
  try:
    updater = Updater(token=bot_token)
    print("  Listen: %s\n"
          "  Port:   %i\n"
          "  URL:    %s" % (webhook_listen, webhook_port, webhook_url))
    update_queue = updater.start_webhook(listen=webhook_listen,
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
  print("Setting up handlers...")
  dispatcher.add_handler(CommandHandler("id", commands.get_id))
  print("Listening.")
  updater.idle()
  print("Stopped")

if __name__ == "__main__":
  if argv_len > 0 and sys.argv[1] == "sanity-check":
    print("success")
    exit(0)
  else:
    start_bot()
