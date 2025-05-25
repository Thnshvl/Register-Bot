import discord
from discord.ext import commands
from db import get_user  # ✅ Using PostgreSQL now

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("❌ Please mention a user to search. Example: `!search @User`")

        result = get_user(member.id)

        if result:
            name, game_id, email = result
            await ctx.send(
                f"🔍 **Registration Info for {member.mention}:**\n"
                f"• **Name**: {name}\n"
                f"• **Game ID**: {game_id}\n"
                f"• **Email**: {email}"
            )
        else:
            await ctx.send(f"⚠️ No registration record found for {member.mention}.")

async def setup(bot):
    await bot.add_cog(Search(bot))
