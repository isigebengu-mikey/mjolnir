import asyncio
import json
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.core import check
intents=discord.Intents.all()
client = commands.Bot(command_prefix='',intents=intents,case_insensitive=True)
with open('config.json', 'r+') as f:
    data = json.load(f)

@client.command('ban')
async def ban(ctx: commands.Context, member: discord.Member):
    if member == ctx.guild.me:
        return await ctx.send("I'm hurt that you would try to ban me...")
    if member.guild_permissions.administrator==True:
        return await ctx.send("Whoops! You can't ban them...")
    else:
        await member.send(f"{ctx.author} used the ban hammer on you, so you're disqualified!")
        await member.ban()

@client.event
async def on_ready():

    client.guild = client.guilds[0]
    client.bancmd = ban
    channel = await client.fetch_channel(int(data['channel']))
    ping = await channel.send('@everyone')
    await ping.delete()
    msg = await channel.send("To ban users, use `ban <member>`! Now go!")
    await channel.send('3...')
    await asyncio.sleep(1)
    await channel.send('2...')
    await asyncio.sleep(1)
    await channel.send('1...')
    await asyncio.sleep(1)
    await channel.send('Go!')
    await channel.set_permissions(channel.guild.default_role, read_messages=True, send_messages=True)
    await check_winner.start()

@client.event
async def on_error(ctx, error: Exception):
    if isinstance(error, commands.DisabledCommand):
        await ctx.send("The event hasn't started yet!")

@tasks.loop(seconds=1)
async def check_winner():
    if len([i for i in client.guilds[0].members if i.guild_permissions.administrator==False]) == 1:
        await client.guilds[0].text_channels[0].send(f'@everyone We have our winner! Congratulations {[i for i in client.guilds[0].members if i.guild_permissions.administrator==False][0]}')
        await check_winner.stop()

client.load_extension('jishaku')
client.run(data['token'])