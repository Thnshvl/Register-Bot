import discord
from discord.ext import commands
import csv

class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Owner", "Mods", "Admins")
    async def edit(self, ctx, member: discord.Member = None, field: str = None, *, new_value: str = None):
        if not member or not field or not new_value:
            return await ctx.send("❗ Usage: `!edit @User field new_value`\nValid fields: `name`, `game_id`, `email`")

        field = field.lower()
        field_map = {"name": 1, "game_id": 2, "email": 3}

        if field not in field_map:
            return await ctx.send("❌ Invalid field. Use one of: `name`, `game_id`, `email`")

        tag = str(member)
        updated = False

        try:
            with open("database.csv", "r") as file:
                rows = list(csv.reader(file))

            with open("database.csv", "w", newline='') as file:
                writer = csv.writer(file)
                for row in rows:
                    if row[0] == tag:
                        row[field_map[field]] = new_value
                        updated = True
                    writer.writerow(row)

            if updated:
                await ctx.send(f"✅ Updated `{field}` for {member.mention} to: `{new_value}`")
            else:
                await ctx.send(f"⚠️ No registration record found for {member.mention}")

        except FileNotFoundError:
            await ctx.send("⚠️ No database file found.")

async def setup(bot):
    await bot.add_cog(Edit(bot))
