import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🛠️ Available Commands",
            description="Here’s a list of all the bot commands and what they do:",
            color=discord.Color.green()
        )

        embed.add_field(
            name="`!register`",
            value="Starts the registration process in a private channel. Asks for name, game ID, and email. Includes confirmation and disclaimer before submitting.",
            inline=False
        )
        embed.add_field(
            name="`!database`",
            value="Shows the full registration database. Only usable by staff roles (Owner, Mods, Admins).",
            inline=False
        )
        embed.add_field(
            name="`!search @User`",
            value="Fetches the registration details of the mentioned user.",
            inline=False
        )
        embed.add_field(
            name="`!delete @User`",
            value="Deletes the entire registration for the mentioned user.",
            inline=False
        )
        embed.add_field(
            name="`!delete @User field`",
            value="Deletes a specific field (name, game_id, or email) from the mentioned user's registration.",
            inline=False
        )
        embed.add_field(
            name="`!edit @User field new_value`",
            value="Edits a specific field in a user's registration. Only usable by staff roles.",
            inline=False
        )
        embed.add_field(
            name="`!help`",
            value="Displays this help menu.",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))

