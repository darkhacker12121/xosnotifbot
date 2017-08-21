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

# Python imports
import os
import sys

# Library imports
import telegram

def get_id(bot, update):
  update.message.reply_text("ID: %s" % update.message.chat_id)

def runs(bot, update):
  update.message.reply_text("Where u going so fast?!")

commands = [
  ["id", get_id],
  ["runs", runs],
]