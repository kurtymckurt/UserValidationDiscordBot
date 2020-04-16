# Requires python3 and pip3
# To run:
#  - pip3 install discord.py
#  - pip3 install python-dotenv
#  - pip3 install tinydb
#
# You need to have a user with the role 'admin' in order to change server defaults with
# !change-role <role>
# !change-server-name "<channel name>"
# !change-channel <channel name>
import os.path
import string
import random
import discord
import discord.utils
import asyncio
from GlobalBotConfig import GlobalBotConfig
from discord import Member
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

validation_channel = os.getenv('VALIDATION_CHANNEL')
validation_role = os.getenv('VALIDATION_ROLE')
admin_role = os.getenv('ADMIN_ROLE')

global_bot_config = GlobalBotConfig.get_instance()


@commands.has_role(admin_role)
@bot.command(name='change-role')
async def change_config_role(ctx, arg='new_user'):
    global_bot_config.add_role(ctx.guild.id, arg)
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
    global_bot_config.add_channel(ctx.guild.id, arg)
    write_log(f'changing to channel to: {arg} {global_bot_config.get_guild_config(ctx.guild.id)}')
    await ctx.channel.send(f'Changed channel  to: {arg}')


@commands.has_role(admin_role)
@bot.command(name='see-config')
async def see_config(ctx):
    server_config = global_bot_config.get_guild_config(ctx.guild.id)
    server_name = server_config['server_name']
    channel = server_config['channel']
    role = server_config['role']
    message = f'Channel: {channel}, Role: {role}, Server name: {server_name}'
    await ctx.channel.send(f'Current discord config: {message}')


@commands.has_role(admin_role)
@bot.command(name='change-rules')
async def see_config(ctx, arg):
    global_bot_config.add_rules(ctx.guild.id, arg)
    write_log(f'changing rules to: {arg}')
    await ctx.channel.send(f'changing rules  to: {arg}')


@bot.event
async def on_member_join(member):
    code = random_string(5).upper()
    global_bot_config.add_user_code(member.guild.id, member.id, code)
    server_config = global_bot_config.get_guild_config(member.guild.id)
    server_name = server_config['server_name']
    channel_name = server_config['channel']
    server_rules = server_config['server_rules']
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {server_name}!'
    )
    await member.dm_channel.send(
        f'Remember to follow the rules! The current rules are: {server_rules}.'
    )
    await member.dm_channel.send(
          f'Go to channel {channel_name} and enter the code {code}'
    )
    await member.dm_channel.send(
          f'By typing the code into the channel, you are agreeing to all rules written and unwritten.'
    )


@bot.event
async def on_guild_join(guild):
    guild_id = guild.id

    if not global_bot_config.exists_guild_config(guild_id):
        global_bot_config.create_guild_config(guild_id)


async def daily_user_check():
    while not bot.is_closed():
        write_log(f'Removing expired users...')
        global_bot_config.delete_expired_users()
        await asyncio.sleep(60)


@bot.event
async def on_guild_remove(guild):
    global_bot_config.delete_guild(guild.id)


@bot.event
async def on_message(message):
    member = message.author
    if isinstance(member, Member):
        guild_id = member.guild.id

        # if we dont have the server configs set up,
        # then do that.
        if not global_bot_config.exists_guild_config(guild_id):
            global_bot_config.create_guild_config(guild_id)

        server_config = global_bot_config.get_guild_config(guild_id)
        role = discord.utils.get(member.guild.roles, name=server_config['role'])
        user_id = member.id
        # if we found the role in the guild
        # and the user is in the required channel
        # and the user entered the code.
        # Then give that user the new user role.
        if role is not None:
            if message.channel.name == server_config['channel']:
                if global_bot_config.exists_user_code(guild_id, user_id):
                    if message.content == global_bot_config.get_user_code(guild_id, user_id):
                        await member.add_roles(role)
                        global_bot_config.delete_user_code(guild_id, user_id)

    await bot.process_commands(message)


def write_log(log_line):
    with open('std.log', 'a') as the_file:
        the_file.write(log_line)
        the_file.write('\n')
        the_file.close()
    print(log_line)


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


print('Starting bot... awaiting commands and messages.')

bot.loop.create_task(daily_user_check())
bot.run(TOKEN)
