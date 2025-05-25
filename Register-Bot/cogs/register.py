import discord
from discord.ext import commands
from db import save_user  # ✅ PostgreSQL function instead of CSV

is_locked = False  # Global toggle for registration lock

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        global is_locked
        if is_locked:
            return await ctx.send("🚫 Registration is currently **locked** by the admins. Please try again later.")

        guild = ctx.guild
        channel_name = f"register-{ctx.author.name}".lower().replace(" ", "-")
        existing = discord.utils.get(guild.text_channels, name=channel_name)

        if existing:
            return await ctx.send("❗ You already have a registration channel open.")

        # Create private channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        category = ctx.channel.category or None  # Use same category or none
        channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            category=category
        )

        await ctx.send(f"📩 Your registration has started in {channel.mention}.")

        def check(m): return m.author == ctx.author and m.channel == channel

        # Ask Name
        await channel.send("Please enter your **Name** (or type `skip`):")
        name_msg = await self.bot.wait_for("message", check=check)
        name = name_msg.content if name_msg.content.lower() != "skip" else "N/A"

        # Game ID
        await channel.send("Please enter your **Game ID**:")
        game_id = await self.bot.wait_for("message", check=check)

        # Email (must contain @)
        while True:
            await channel.send("Please enter your **Email**:")
            email = await self.bot.wait_for("message", check=check)
            if "@" in email.content:
                break
            else:
                await channel.send("❌ Invalid email. Try again.")

        # Confirm
        await channel.send(
            f"📋 **Review your information:**\n"
            f"• Name: {name}\n"
            f"• Game ID: {game_id.content}\n"
            f"• Email: {email.content}\n\n"
            f"📜 By registering, you agree to the server rules. Your information—especially the Game ID—will be permanently linked to your Discord account and cannot be changed, in order to prevent smurfing and the use of alternate accounts. "
            f"Type `accept` to continue or `cancel` to stop."
        )

        while True:
            confirm = await self.bot.wait_for("message", check=check)
            if confirm.content.lower() == "accept":
                break
            elif confirm.content.lower() == "cancel":
                await channel.send("❌ Registration cancelled.")
                return await channel.delete()
            else:
                await channel.send("Please type `accept` or `cancel`.")

        # Role updates
        member_role = discord.utils.get(guild.roles, name="Member")
        unreg_role = discord.utils.get(guild.roles, name="Unregistered")
        if unreg_role in ctx.author.roles:
            await ctx.author.remove_roles(unreg_role)
        if member_role:
            await ctx.author.add_roles(member_role)

        # Log and save
        log_channel = discord.utils.get(guild.text_channels, name="registration-log")
        if log_channel:
            await log_channel.send(
                f"📋 **New Registration**\nUser: {ctx.author.mention}\nName: {name}\nGame ID: {game_id.content}\nEmail: {email.content}"
            )

        # ✅ Save to PostgreSQL instead of CSV
        save_user(str(ctx.author), ctx.author.id, name, game_id.content, email.content)

        await channel.send("✅ Registration complete. This channel will now be deleted.")
        await channel.delete()

    @commands.command()
    @commands.has_any_role("Owner", "Mods", "Admins")
    async def lockregister(self, ctx):
        global is_locked
        is_locked = True
        await ctx.send("🔒 `!register` command has been **locked**. New users cannot register at this time.")

    @commands.command()
    @commands.has_any_role("Owner", "Mods", "Admins")
    async def unlockregister(self, ctx):
        global is_locked
        is_locked = False
        await ctx.send("🔓 `!register` command has been **unlocked**. Users may now register again.")

async def setup(bot):
    await bot.add_cog(Register(bot))

