import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🛠️ Available Commands",
            description="Here's a list of all commands and what they do:",
            color=discord.Color.green()
        )

        embed.add_field(
            name="`!register`",
            value="Starts the registration process. Asks for name, game ID, and email, with review and disclaimer.",
            inline=False
        )
        embed.add_field(
            name="`!database`",
            value="Shows the full registration database. Only accessible to staff roles.",
            inline=False
        )
        embed.add_field(
            name="`!search @User`",
            value="Searches and displays the registration details of a mentioned user.",
            inline=False
        )
        embed.add_field(
            name="`!delete @User`",
            value="Deletes a user's entire registration entry. You can also delete specific fields using: `!delete @User field`.",
            inline=False
        )
        embed.add_field(
            name="`!help`",
            value="Displays this help menu with brief descriptions of each command.",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
