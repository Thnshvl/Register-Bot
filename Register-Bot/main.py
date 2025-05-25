import discord
from db import setup  # Already here - good
from discord.ext import commands
from keep_alive import keep_alive
import os
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')  # Disable default help so we can use custom one

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Access denied. You do not have the required role to use this bot.")
    else:
        raise error

@bot.event
async def on_ready():
    setup()  # ✅ This sets up your PostgreSQL table
    print(f'{bot.user} is online!')

@bot.event
async def on_member_join(member):
    unregistered_role = discord.utils.get(member.guild.roles, name="Unregistered")
    if unregistered_role:
        await member.add_roles(unregistered_role)

async def load_extensions():
    await bot.load_extension("cogs.register")
    await bot.load_extension("cogs.database")
    await bot.load_extension("cogs.search")  
    await bot.load_extension("cogs.delete")
    await bot.load_extension("cogs.edit")
    await bot.load_extension("cogs.help")

keep_alive()

async def main():
    await load_extensions()
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
