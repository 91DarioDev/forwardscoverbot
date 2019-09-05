# ForwardsCoverBot

This telegram bot just echoes any message you send it or modify for him. If you don't like telegram forwards, before sending a message, send the message to the bot, then forward the message that the bot returns to the user you were chatting with. In case he will forward the message, it will have the name of the bot in the forward label. It supports anything and respect the formatting style of the text.

## How to run this bot by you:
To be sure that when you send messages to this bot to anonymize them it doesn't forward your message in other chats (it doesn't), you may want to run a your own instance.

**If you want to run this bot by you:**


**Clone and install:**
```
cd path
git clone https://github.com/91DarioDev/forwardscoverbot
cd forwardscoverbot
pip install .
```

**Config the bot:**
- open `forwardscoverbot/config/config.example.yaml`
- select all and copy
- create a file `forwardscoverbot/config/config.yaml`
- paste and replace the values with real values
- save and close

**Run the bot:**
```
forwardscoverbot
```
Note: _In case you want to call forwardscoverbot from another path, you can, but you have to specify the path of the config.yaml file as first argument in the cli.
Example:_

```
fowardscoverbot path/forwardscoverbot/config/config.yaml
```

**Upgrade the bot:**
```
cd path/forwardscoverbot
git pull https://github.com/91DarioDev/forwardscoverbot
pip install --upgrade .
```

## How to use it:

- send messages to the bot to get echoed messages

**Commands:**

- `/start`, `/help` - replies with a welcome message
- `/disablewebpagepreview`- remove the link preview from an echoed message
- `/stats` - get statistics about the use of the bot (admins only)
- `/removecaption` - remove caption from a message
- `/addcaption` - add or overwrite a caption to a message
- `/removebuttons` - remove buttons from a message
