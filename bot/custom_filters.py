
# Library imports
from telegram.ext import BaseFilter

class HashMessageFilter(BaseFilter):
  def filter(self, message):
    return len(message.text) >= 2 and message.text[0] == '#'

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
