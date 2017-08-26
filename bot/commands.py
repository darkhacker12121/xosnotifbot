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
import requests
from subprocess import call
from os.path import expanduser

# Library imports
import telegram

# Project imports
from utils import getenviron

def get_id(bot, update):
    update.message.reply_text("ID: %s" % update.message.chat_id)

def runs(bot, update):
    update.message.reply_text("Where u going so fast?!")

_jenkins_address = getenviron("NOLIFER_JENKINS_ADDR", "localhost")
_jenkins_port = int(getenviron("NOLIFER_JENKINS_PORT", "6692"))
_jenkins_user = getenviron("NOLIFER_JENKINS_USER", "xdevs23")
_jenkins_project = getenviron("NOLIFER_JENKINS_PROJECT", "halogenOS")
_jenkins_ssh_key = getenviron("NOLIFER_JENKINS_SSHKEY",
                              "%s/.ssh/id_rsa" % expanduser("~"))
_jenkins_rom_ver_param = getenviron("NOLIFER_ROM_VER_PARAM", "XOS_Version")
_rom_versions = getenviron("NOLIFER_ROM_VERSIONS", "8.0,7.1").split(",")
_github_auth_token = getenviron("NOLIFER_GITHUB_TOKEN", "")
def launch_build(bot, update):
    # Family group or my private chat
    if update.message.chat_id == -1001068076699 or \
       update.message.chat_id == 11814515:
        msg_no_split = update.message.text[len("/build "):]
        if "'" in msg_no_split or '"' in msg_no_split or ";" in msg_no_split:
            update.message.reply_text("Don't even try")
            return
        split_msg = msg_no_split.split()
        final_command = "ssh -l %s -i %s %s -p %i build %s" \
                    % (
                         _jenkins_user,
                         _jenkins_ssh_key,
                         _jenkins_address,
                         _jenkins_port,
                         _jenkins_project
                        )
        human_friendly_description = ""
        if split_msg:
            target_device = split_msg[0]
            page = 1
            api_url_tpl = 'https://api.github.com/orgs/halogenOS/repos?page=%s'
            r = None
            if _github_auth_token != "":
                print("GitHub authorization token available.")
                r = requests.get(api_url_tpl % page, headers={
                    'Authorization': 'token %s' % _github_auth_token
                })
            else:
                r = requests.get(api_url_tpl % page)
            has_found_device = False
            while not has_found_device and r.json():
                if "message" in r.json() and \
                    "API rate limit exceeded" in r.json()["message"]:
                        update.message.reply_text(
                            "API rate limit exceeded for my IP, can't check "
                            "whether the device tree exists"
                        )
                        return
                for entry in r.json():
                    if "name" in entry:
                        print(entry["name"])
                        if entry["name"] != None and \
                                "android_device_" in entry["name"] and \
                                target_device in entry["name"]:
                            print("Found %s" % entry["name"])
                            has_found_device = True
                            break
                page += 1
                if _github_auth_token != "":
                    r = requests.get(api_url_tpl % page, headers={
                        'Authorization': 'token %s' % _github_auth_token
                    })
                else:
                    r = requests.get(api_url_tpl % page)
            if not has_found_device:
                update.message.reply_text(
                    "Device %s does not exist on our org" % target_device)
                return
            final_command += " -p 'Target_device=%s'" % target_device
            human_friendly_description += "Device: %s\n" % target_device
            is_release = False
            if len(split_msg) >= 2:
                split_msg.remove(target_device)
                if "noclean" in split_msg:
                    final_command += " -p 'do_clean=false'"
                    split_msg.remove("noclean")
                    human_friendly_description += "No clean\n"
                if "noreset" in split_msg:
                    final_command += " -p 'do_not_reset=true'"
                    split_msg.remove("noreset")
                    human_friendly_description += "No git reset\n"
                if "release" in split_msg:
                    final_command += \
                        " -p " \
                        "'Prepare_for_official_release=true' -p " \
                        "'Do_release=true' -p " \
                        "'Auto_release=true'"
                    split_msg.remove("release")
                    is_release = True

                build_type = "userdebug"
                if "user" in split_msg:
                    build_type = "user"
                elif "eng" in split_msg:
                    build_type = "eng"

                rom_version = _rom_versions[0]

                for ver in _rom_versions:
                    if ver in split_msg:
                        rom_version = ver
                        split_msg.remove(ver)
                        break

                final_command += " -p '%s=%s'" % \
                                    (_jenkins_rom_ver_param, rom_version)
                human_friendly_description += "ROM Version: %s\n" % rom_version

                if build_type in split_msg:
                    split_msg.remove(build_type)
                human_friendly_description += "Build type: %s\n" % build_type

                final_command += " -p 'Build_type=%s'" % build_type

                repopick_list = ""
                module_to_build = ""
                had_repopick = False
                for arg in split_msg:
                    if had_repopick: break
                    if "repopick" in arg:
                        start_repopick_ix = split_msg.index(arg)
                        j = start_repopick_ix + 1
                        while j < len(split_msg):
                            if split_msg[j] != "-t":
                                repopick_list += "%s," % split_msg[j]
                                if j == len(split_msg) - 1:
                                    repopick_list = repopick_list[:-1]
                            else:
                                repopick_list += \
                                    "[[NEWLINE]]-t %s[[NEWLINE]]" \
                                        % split_msg[j + 1]
                                if j + 1 == len(split_msg) - 1:
                                    repopick_list = \
                                        repopick_list[:-(len("[[NEWLINE]]"))]
                                j += 1
                            j += 1
                        had_repopick = True
                        repopick_list.replace(
                            "[[NEWLINE]][[NEWLINE]]", "[[NEWLINE]]")
                    elif not module_to_build:
                        module_to_build = arg
                    else:
                        update.message.reply_text(
                            "Could not understand your request. "
                            "Unrecognized argument %s" % arg)
                        return

                if had_repopick:
                    final_command += " -p 'repopick_before_build=%s'" \
                                        % repopick_list
                    human_friendly_description += "Stuff to repopick:\n%s\n" \
                                                        % repopick_list
                if module_to_build:
                    final_command += " -p 'Module_to_build=%s'" % \
                                        module_to_build
                    human_friendly_description += "Module: %s\n" % \
                                                    module_to_build
        else:
            update.message.reply_text(
                "Please specify a device like: /build oneplus2")
            return
        result_ = call(final_command.split())
        if not result_:
            update.message.reply_text("%s build launched\n\n%s" \
                                        % ("Release" if is_release else "Test",
                                            human_friendly_description.replace(
                                                "[[NEWLINE]]", "\n")))
        else:
            update.message.reply_text("Cannot launch build, error code %i",
                                        result_)

commands = [
    ["id", get_id],
    ["runs", runs],
    ["build", launch_build],
]