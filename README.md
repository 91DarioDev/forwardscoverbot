# ForwardsCoverBot

This telegram bot just echoes any message you send it or modify for him. If you don't like telegram forwards, before sending a message, send the message to the bot, then forward the message that the bot returns to the user you were chatting with. In case he will forward the message, it will have the name of the bot in the forward label. It supports anything and respect the formatting style of the text.

## How to run this bot by you:
To be sure that when you send messages to this bot to anonymize them it doesn't forward your message in other chats (it doesn't), you may want to run a your own instance.

**If you want to run this bot by you:**


**Clone and install:**
```
git clone https://github.com/91DarioDev/forwardscoverbot
cd forwardscoverbot
pip install .
```

**Config the bot:**
- open `forwardscoverbot/config/config.example.yaml`
- select all and copy
- create a file `forwardscoverbot/config/config.yaml`
- replace the values with real values
- save and close

**Run the bot:**
```
forwardscoverbot
```

**Upgrade the bot:**
```
git pull https://github.com/91DarioDev/forwardscoverbot
cd forwardscoverbot
pip install .
```

