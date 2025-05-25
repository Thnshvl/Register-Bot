import discord
from discord.ext import commands
from db import delete_user, update_field  # ✅ PostgreSQL functions

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete(self, ctx, member: discord.Member = None, field: str = None):
        if member is None:
            return await ctx.send("❌ Please mention a user. Example: `!delete @User` or `!delete @User email`")

        field = field.lower() if field else None
        valid_fields = ["name", "game_id", "email"]

        if field and field not in valid_fields:
            return await ctx.send("❌ Invalid field. Use: `name`, `game_id`, or `email`.")

        if field:
            success = update_field(member.id, field, "N/A")
            if success:
                await ctx.send(f"✅ Deleted `{field}` from {member.mention}'s registration.")
            else:
                await ctx.send(f"⚠️ No registration record found for {member.mention}.")
        else:
            delete_user(member.id)
            await ctx.send(f"✅ Deleted all registration data for {member.mention}.")

async def setup(bot):
    await bot.add_cog(Delete(bot))

