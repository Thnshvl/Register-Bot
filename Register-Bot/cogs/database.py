import discord
from discord.ext import commands
import csv

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def database(self, ctx):
        allowed_roles = ["Owner", "Mods", "Admins"]
        if not any(role.name in allowed_roles for role in ctx.author.roles):
            return await ctx.send("❌ You don’t have permission to use this command.")

        try:
            with open("database.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)

                if not rows:
                    return await ctx.send("📂 The registration database is empty.")

                message = "**📋 Registration Database:**\n"
                for i, row in enumerate(rows, start=1):
                    message += f"{i}. **User**: {row[0]} | **Name**: {row[1]} | **Game ID**: {row[2]} | **Email**: {row[3]}\n"

                if len(message) > 1900:
                    await ctx.author.send(message)
                    await ctx.send("📬 Sent the database to your DMs.")
                else:
                    await ctx.send(message)

        except FileNotFoundError:
            await ctx.send("⚠️ No database found. No one has registered yet.")

async def setup(bot):
    await bot.add_cog(Database(bot))
