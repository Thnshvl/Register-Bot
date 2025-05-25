import discord
from discord.ext import commands
from db import update_field  # ✅ Use PostgreSQL instead of CSV

class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Owner", "Mods", "Admins")
    async def edit(self, ctx, member: discord.Member = None, field: str = None, *, new_value: str = None):
        if not member or not field or not new_value:
            return await ctx.send("❗ Usage: `!edit @User field new_value`\nValid fields: `name`, `game_id`, `email`")

        field = field.lower()
        if field not in ["name", "game_id", "email"]:
            return await ctx.send("❌ Invalid field. Use one of: `name`, `game_id`, `email`")

        success = update_field(member.id, field, new_value)

        if success:
            await ctx.send(f"✅ Updated `{field}` for {member.mention} to: `{new_value}`")
        else:
            await ctx.send(f"⚠️ No registration record found for {member.mention}")

async def setup(bot):
    await bot.add_cog(Edit(bot))

