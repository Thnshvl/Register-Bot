import discord
from discord.ext import commands
import csv

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete(self, ctx, member: discord.Member = None, field: str = None):
        if member is None:
            return await ctx.send("❌ Please mention a user. Example: `!delete @User` or `!delete @User email`")

        tag = str(member)
        found = False

        try:
            # Read all entries
            with open("database.csv", "r") as file:
                rows = list(csv.reader(file))

            # Rewrite with updated or removed info
            with open("database.csv", "w", newline='') as file:
                writer = csv.writer(file)

                for row in rows:
                    if row[0] == tag:
                        found = True

                        if field is None:
                            # Skip writing this row = delete full entry
                            continue
                        elif field.lower() == "name":
                            row[1] = "N/A"
                        elif field.lower() == "game_id":
                            row[2] = "N/A"
                        elif field.lower() == "email":
                            row[3] = "N/A"
                        else:
                            await ctx.send("❌ Invalid field. Use: `name`, `game_id`, or `email`.")
                            return

                    writer.writerow(row)

            if found:
                if field:
                    await ctx.send(f"✅ Deleted `{field}` from {member.mention}'s registration.")
                else:
                    await ctx.send(f"✅ Deleted all registration data for {member.mention}.")
            else:
                await ctx.send(f"⚠️ No registration record found for {member.mention}.")

        except FileNotFoundError:
            await ctx.send("⚠️ No database file found.")

async def setup(bot):
    await bot.add_cog(Delete(bot))
