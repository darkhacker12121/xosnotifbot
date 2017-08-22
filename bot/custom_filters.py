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

# Library imports
from telegram.ext import BaseFilter

class HashMessageFilter(BaseFilter):
  def filter(self, message):
    return message.text != None and \
            len(message.text) >= 2 and message.text[0] == '#'

def on_hash_message(bot, update):
  msg_split = update.message.text.split()
  hashtag_item = msg_split[0][1:]
  if update.message.chat_id == -1001068076699:
    if hashtag_item == "latest":
      try:
        file = open("/var/lib/jenkins/workspace/halogenOS/oneplus2-latest.txt",
                    "r")
        update.message.reply_text(file.read())
        file.close()
      except Exception as e:
        print("Error while getting latest: %s" % e)
    elif hashtag_item == "modem":
      update.message.reply_text("https://www.androidfilehost.com/?fid=889764386195914770")

hash_message_filter = HashMessageFilter()

filters = [
  [hash_message_filter, on_hash_message],
]
