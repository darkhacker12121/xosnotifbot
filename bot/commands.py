
# Python imports
import os
import sys

# Library imports
import telegram

def get_id(bot, update):
  update.message.reply_text("ID: %s" % update.message.chat_id)