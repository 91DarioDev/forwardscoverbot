# Forwards-Pics-Bot

This code is forked from:

```
https://github.com/91DarioDev/forwardscoverbot
```

## You should know:

This code is base on the python3 and pip3

So, just install the pip3 and use the pip3 replace the pip2

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

- `/help`   - replies with a welcome message

- `/random` - show a photo random

## And if you are the administrator:

- `/Show`                   - show the administrator's message, full and wide

- `/ForwardStateTransition` - forware message or not

- `/CheckExistedOrNot`      - check the mysql if this picture has the same value

- `/CheckResultShow`        - if turn this off, it will not show you the check result message if the value is unique

- `/CheckAllData`           - not in the default code, but it can be check all the data in mysql unique

## Clone and install:
```
cd path
git clone https://github.com/rikonaka/forwards-pics-bot.git
cd forwards-pics-bot
pip3 install --upgrade .
```

## Config the bot:

- into `forwards-pics-bot/config`

- copy to a new file like ` cp config.example.yaml config.yaml `

- edit and replace the values with work values

- save and close

## Run the bot:

```
bot /path/config.yaml
```

## Upgrade the bot:

```
cd /path/forwards-pics-bot
git pull
pip install --upgrade .
```

