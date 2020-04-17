# UserValidationDiscordBot

# Setup

There are two ways to configure:

First, you need to fill the .env with the proper environment variables.
DISCORD_TOKEN, ADMIN_ROLE, VALIDATION_CHANNEL, and VALIDATION_ROLE

* DISCORD_TOKEN is the token you get from making the application using the discord development portal
* ADMIN_ROLE is the role of the users that can configure the bot.
* VALIDATION_CHANNEL is the default channel the bot will use to accept codes
* VALIDATION_ROLE is the default role the bot will attempt to hand out  

OR

You can add these to the command line environment:

```export DISCORD_TOKEN=<token>```

```export ADMIN_ROLE=<role>```

```export VALIDATION_CHANNEL=<channel>```

```export VALIDATION_ROLE=<role>```


Lastly, but also the most important.  The bot requires a role that can modify roles. That role must be HIGHER than the
role the bot will hand out.  So when you look for the discord roles, you can drag them in order. Move the bots role above 
the role listed in VALIDATION_ROLE.


# Running the bot
## Docker
We now provide a docker file so you can run your own docker version of the bot.
I recommend bind mounting a directory so that you can use the same json file to read/write from.
It acts as a database for the bot.  By default it chooses ./db.json.

### Commands:
 docker build -t user_validation_bot .
 docker run -d user_validation_bot:latest --name user_validation_bot

## Manual Setup
- Install python3
- Install pip3
- pip3 install discord.py
- pip3 install python-dotenv
- pip3 install tinydb
- Fill in var in .env file

To change bot defaults, your user needs whatever role you specify in the .env file

### Commands
python3 bot.py

# How to use available commands

Once you have the bot running, you can run several commands to setup the bot more specific to your discord server.


To change what the server name says when the bot DMs a user, use the following command:

``!change-server-name "<server-name>"``


To change what role is given to a user when they validate, use the following command:

``!change-role <role>``


To change what channel the user has to type their code in to validate, use the following command:


``!change-channel <channel>``
