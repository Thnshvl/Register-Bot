import discord
from discord.ext import commands
from db import get_all_users  # ✅ PostgreSQL version

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def database(self, ctx):
        allowed_roles = ["Owner", "Mods", "Admins"]
        if not any(role.name in allowed_roles for role in ctx.author.roles):
            return await ctx.send("❌ You don’t have permission to use this command.")

        users = get_all_users()

        if not users:
            return await ctx.send("📂 The registration database is empty.")

        message = "**📋 Registration Database:**\n"
        for i, user in enumerate(users, start=1):
            discord_tag, name, game_id, email = user
            message += f"{i}. **User**: {discord_tag} | **Name**: {name} | **Game ID**: {game_id} | **Email**: {email}\n"

        if len(message) > 1900:
            await ctx.author.send(message)
            await ctx.send("📬 Sent the database to your DMs.")
        else:
            await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Database(bot))
