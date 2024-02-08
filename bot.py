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
import discord
import discord.utils
import asyncio
import sys
from GlobalBotConfig import GlobalBotConfig
from discord import Member
from discord.ext import commands
from dotenv import load_dotenv
import secrets

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

validation_channel = os.getenv('VALIDATION_CHANNEL')
validation_role = os.getenv('VALIDATION_ROLE')
admin_role = os.getenv('ADMIN_ROLE')
welcome_channel = os.getenv('WELCOME_CHANNEL')


filename = "db.json"
if len(sys.argv) >= 2:
    filename = sys.argv[1]

global_bot_config = GlobalBotConfig.get_instance(filename)


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


@bot.command(name='rules')
async def get_rules(ctx):
    server_config = global_bot_config.get_guild_config(ctx.guild.id)
    server_rules = server_config['server_rules']
    await ctx.channel.send(f'{server_rules}')


@bot.command(name='commands')
async def send_commands(ctx):
    message = ' Admin commands: change-server-name <name>, change-role <role>, change-channel <channel name>  ' \
              ' Global commands: rules, resend-code, see-config'
    await ctx.channel.send(f'{message}')


@bot.command(name='resend-code')
async def resend_code(ctx):
    member = ctx.message.author
    code = global_bot_config.get_user_code(ctx.guild.id, member.id)
    if code is None:
        code = random_string(5).upper()
        global_bot_config.add_user_code(member.guild.id, member.id, code)
    await send_code(member, code)


@commands.has_role(admin_role)
@bot.command(name='see-config')
async def see_config(ctx):
    server_config = global_bot_config.get_guild_config(ctx.guild.id)
    server_name = server_config['server_name']
    channel = server_config['channel']
    role = server_config['role']
    server_rules = server_config['server_rules']
    message = f'Channel: {channel}, Role: {role}, Server name: {server_name}, rules: {server_rules}'
    await ctx.channel.send(f'Current discord config: {message}')


@commands.has_role(admin_role)
@bot.command(name='change-rules')
async def change_rules(ctx, arg):
    global_bot_config.add_rules(ctx.guild.id, arg)
    write_log(f'changing rules to: {arg}')
    await ctx.channel.send(f'changing rules  to: {arg}')


@bot.event
async def on_member_join(member):
    code = random_string(5).upper()
    global_bot_config.add_user_code(member.guild.id, member.id, code)
    await send_code(member, code)


async def send_code(member, code):
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
        await asyncio.sleep(86400)


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
                        channel = discord.utils.get(member.guild.channels, name=welcome_channel)
                        await channel.send(f'Welcome {member.display_name} to the discord!')
                admin_role_obj = discord.utils.get(member.guild.roles, name=admin_role)
                if admin_role_obj not in member.roles:
                    await message.delete()

    await bot.process_commands(message)


def write_log(log_line):
    with open('std.log', 'a') as the_file:
        the_file.write(log_line)
        the_file.write('\n')
        the_file.close()
    print(log_line)


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(secrets.SystemRandom().choice(letters) for i in range(string_length))


print('Starting bot... awaiting commands and messages.')

bot.loop.create_task(daily_user_check())
bot.run(TOKEN)
