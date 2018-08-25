# Forwards-Pics-Bot

This code is forked from:
```
https://github.com/91DarioDev/forwardscoverbot
```

## Features:

- Forward a channel photo message to this bot and bot will auto forward it to your groups

- Set the MySQL database for this bot, and it will store every photo in MySQL which you forwarded to it

- Use the `/random` command let the bot show an random photo of your database(if the database has been setting)

## Setting

Here are some setting parameter in the config.yaml

Fill in your bot token here
```
bot_token: "token"
```

Fill in your administrator's telegram id here
```
admins: 
- 1234
```

Fill in the name which groups bot inside(avoid this bot forwarded other groups message)
```
admins_group:
- somegroupid
```

Fill in your groups name or telegram id
```
chat_id: "id"
```

Fill you MySQL info here
```
sql_server: "localhost"
sql_user: "hatsune"
sql_password: "test@test"
sql_database: "hatsunebot"
sql_format: "h_"
max_rows: 1000
```
*The max_rows is mean how many items you want to stored in one tables*
*If seting max_rows as 1000, bot will insert 1000 items in h_pic_0*
*Then, bot will create new table like h_pic_1*

## Commands:

- `/start`, `/help` - replies with a welcome message

- `/turn_off_mysql` - not store every photo

- `/turn_on_mysql`  - start store

- `/stop_forward`   - not forward you message to the groups

- `/start_forward`  - forward

- `/random`         - show a photo random

## Clone and install:
```
cd path
git clone https://github.com/rikonaka/forwards-pics-bot.git
cd forwards-pics-bot
pip3 install --upgrade .
```

## Config the bot:
- open `forwards-pics-bot/config/config.example.yaml`
- select all and copy
- create a file `forwards-pics-bot/config/config.yaml`
- paste and replace the values with real values
- save and close

## Run the bot:
```
hatsune /path/config.yaml
```

## Upgrade the bot:
```
cd /path/forwards-pics-bot
git pull
pip install --upgrade .
```

