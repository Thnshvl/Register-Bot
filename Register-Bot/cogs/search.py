import discord
from discord.ext import commands
import csv

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("❌ Please mention a user to search. Example: `!search @User`")

        tag = str(member)  # e.g., JohnDoe#1234

        try:
            with open("database.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == tag:
                        return await ctx.send(
                            f"🔍 **Registration Info for {member.mention}:**\n"
                            f"• **Name**: {row[1]}\n"
                            f"• **Game ID**: {row[2]}\n"
                            f"• **Email**: {row[3]}"
                        )

                await ctx.send(f"⚠️ No registration record found for {member.mention}.")

        except FileNotFoundError:
            await ctx.send("⚠️ No database found. No one has registered yet.")

async def setup(bot):
    await bot.add_cog(Search(bot))
