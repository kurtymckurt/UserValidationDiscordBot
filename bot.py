# Requires python3 and pip3
# To run:
#  - pip3 install discord.py
#  - pip3 install python-dotenv
#  - pip3 install jsonpickle
#
# You need to have a user with the role 'admin' in order to change server defaults with
# !change-role <role>
# !change-server-name "<channel name>"
# !change-channel <channel name>


import os.path
import jsonpickle
import string
import random
import discord
import discord.utils
from GlobalBotConfig import GlobalBotConfig
from ServerConfig import ServerConfig
from discord import Member
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

validation_channel = os.getenv('VALIDATION_CHANNEL')
validation_role = os.getenv('VALIDATION_ROLE')
admin_role = os.getenv('ADMIN_ROLE')

global_bot_config = GlobalBotConfig()


@commands.has_role(admin_role)
@bot.command(name='change-role')
async def change_config_role(ctx, arg='new_user'):
    global_bot_config.get_guild_config(ctx.guild.id).role = arg
    write_log(f'changing to role to: {arg} {global_bot_config.get_guild_config(ctx.guild.id)}')
    await ctx.channel.send(f'Changed new user role to: {arg}')


@commands.has_role(admin_role)
@bot.command(name='change-server-name')
async def change_server_name(ctx, arg='my Discord Server'):
    global_bot_config.add_server_name(ctx.guild.id, arg)
    write_log(f'changing to server name to: {arg}')
    await ctx.channel.send(f'Changed server name to: {arg}')


@commands.has_role(admin_role)
@bot.command(name='change-channel')
async def change_channel(ctx, arg='guest'):
    global_bot_config.get_guild_config(ctx.guild.id).channel = arg
    write_log(f'changing to channel to: {arg} {global_bot_config.get_guild_config(ctx.guild.id)}')
    await ctx.channel.send(f'Changed channel  to: {arg}')


@bot.event
async def on_member_join(member):
    code = random_string(5).upper()
    global_bot_config.add_user_code(member.id, code)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {global_bot_config.get_server_name(member.guild.id)}! '
        f'Go to channel {global_bot_config.get_guild_config(member.guild.id).channel} and enter the code {code}'
    )


@bot.event
async def on_message(message):
    member = message.author
    if isinstance(member, Member):
        guild_id = member.guild.id

        # if we dont have the server configs set up,
        # then do that.
        if not global_bot_config.exists_server_name(guild_id):
            global_bot_config.add_server_name(guild_id, 'my Discord Server')

        if not global_bot_config.exists_guild_config(guild_id):
            global_bot_config.add_guild_config(guild_id, ServerConfig(validation_channel,
                                                                      validation_role))

        server_config = global_bot_config.get_guild_config(guild_id)
        role = discord.utils.get(member.guild.roles, name=server_config.role)
        user_id = member.id
        # if we found the role in the guild
        # and the user is in the required channel
        # and the user entered the code.
        # Then give that user the new user role.
        if role is not None:
            if message.channel.name == server_config.channel:
                if global_bot_config.exists_user_code(user_id):
                    if message.content == global_bot_config.get_user_code(user_id):
                        global_bot_config.delete_user_code(user_id)
                        await member.add_roles(role)
        else:
            write_log(f'Role {server_config.role} was not found in the guild.')

    await bot.process_commands(message)


def write_log(log_line):
    with open('std.log', 'a') as the_file:
        the_file.write(log_line)
        the_file.write('\n')
        the_file.close()


def write_config(config, filename):
    with open(filename, 'w') as the_file:
        the_file.write(jsonpickle.encode(config))
        the_file.close()


def read_config(filename):
    with open(filename, 'r') as the_file:
        json_file = the_file.readline()
        config_json = jsonpickle.decode(json_file, classes=[GlobalBotConfig, ServerConfig])
        return config_json


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


print('Starting bot... awaiting commands and messages.')

if os.path.exists('bot.conf'):
    global_bot_config = read_config('bot.conf')

try:
    bot.run(TOKEN)
except RuntimeError:
    pass
finally:
    write_config(global_bot_config, 'bot.conf')
