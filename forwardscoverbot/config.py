# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2019  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# ForwardsCoverBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ForwardsCoverBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ForwardsCoverBot.  If not, see <http://www.gnu.org/licenses/>


import yaml
import sys


path = "config/config.yaml"
if len(sys.argv) == 2:
    path = sys.argv[1]
try:
    with open(path, 'r') as stream:
        conf = yaml.load(stream)
except FileNotFoundError:
    print("\n\WARNING:\n"
            "before of running forwardscoverbot you should create a file named `config.yaml`"
            " in `config`.\n\nOpen `config/config.example.yaml`\ncopy all\ncreate a file "
            "named `config.yaml`\nPaste and replace sample variables with true data."
            "\nIf the file is in another path, you can specify it as the first parameter."
            "\nExample: <forwardscoverbot /home/my_files/config.yaml>")
    sys.exit()

BOT_TOKEN = conf['bot_token']
DB_PATH = conf['db_path']
ADMINS = conf['admins']
