# UserValidationDiscordBot

# Docker
We now provide a docker file so you can run your own docker version of the bot.
I recommend bind mounting a directory so that you can use the same json file to read/write from.
It acts as a database for the bot.  By default it chooses ./db.json.

## To run:
 docker build -t user_validation_bot .
 docker run -d user_validation_bot:latest --name user_validation_bot

# Manual Setup
- Install python3
- Install pip3
- pip3 install discord.py
- pip3 install python-dotenv
- pip3 install tinydb
- Fill in var in .env file

To change bot defaults, your user needs whatever role you specify in the .env file

## Run
python3 bot.py
