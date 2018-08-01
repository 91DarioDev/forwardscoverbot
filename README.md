# Forwards-Pics-Bot

This code is forked from:
```
https://github.com/91DarioDev/forwardscoverbot
```


**Clone and install:**
```
cd path
git clone https://github.com/rikonaka/forwards-pics-bot.git
cd forwards-pics-bot
pip install .
```

**Config the bot:**
- open `forwards-pics-bot/config/config.example.yaml`
- select all and copy
- create a file `forwardscoverbot/config/config.yaml`
- paste and replace the values with real values
- save and close

**Run the bot:**
```
bot
```


**Upgrade the bot:**
```
cd path/forwardscoverbot
git pull https://github.com/rikonaka/forwards-pics-bot.git
pip install --upgrade .
```

## How to use it:

- send messages to the bot

- and this bot will send you messages to the group at you set's time

**Commands:**

- `/start`, `/help` - replies with a welcome message
- `/disablewebpagepreview`- remove the link preview from an echoed message
- `/stats` - get statistics about the use of the bot (admins only)
- `/removecaption` - remove caption from a message
- `/addcaption` - add or overwrite a caption to a message