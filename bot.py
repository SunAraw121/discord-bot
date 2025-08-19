import os, asyncio
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True          
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)



async def ensure_logs_channel(guild: discord.Guild) -> discord.TextChannel | None:
 
    for ch in guild.text_channels:
        if ch.name.lower() == "logs":
            return ch
    return None

async def ensure_muted_role(guild: discord.Guild) -> discord.Role:
    role = discord.utils.get(guild.roles, name="Muted")
    if role:
        return role
    role = await guild.create_role(name="Muted", reason="Create Muted role for moderation")

    for channel in guild.channels:
        try:
            await channel.set_permissions(role, send_messages=False, speak=False, add_reactions=False)
        except Exception:
            pass
    return role

@bot.event
async def on_ready():
    print(f"{bot.user} is online in {len(bot.guilds)} server(s).")

@bot.event
async def on_member_join(member: discord.Member):

    channel = discord.utils.find(lambda c: isinstance(c, discord.TextChannel) and c.permissions_for(member.guild.me).send_messages, member.guild.text_channels)
    if channel:
        await channel.send(f"Welcome {member.mention}! 🎉")

@bot.event
async def on_message_delete(message: discord.Message):

    log_ch = await ensure_logs_channel(message.guild)
    if log_ch:
        author = getattr(message.author, "mention", "Unknown")
        content = message.content if message.content else "(content unavailable)"
        await log_ch.send(f"🗑️ Message deleted by {author} in {message.channel.mention}:\n{content}")

@bot.command(help="Ban a member. Usage: !ban @user [reason]")
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason: str | None = None):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 {member} has been banned. Reason: {reason or 'None'}")

@bot.command(help="Unban a user by name#discriminator or name only. Usage: !unban username#1234")
@commands.has_permissions(ban_members=True)
async def unban(ctx: commands.Context, *, member_name: str):
    bans = await ctx.guild.bans()
    target = None
    for ban_entry in bans:
        user = ban_entry.user
        if member_name.lower() in (f"{user.name}#{user.discriminator}".lower(), user.name.lower()):
            target = user
            break
    if target:
        await ctx.guild.unban(target)
        await ctx.send(f" Unbanned {target}")
    else:
        await ctx.send("User not found in ban list.")

@bot.command(help="Mute a member for N minutes (default 5). Usage: !mute @user [minutes]")
@commands.has_permissions(manage_roles=True)
async def mute(ctx: commands.Context, member: discord.Member, minutes: int = 5):
    mute_role = await ensure_muted_role(ctx.guild)
    await member.add_roles(mute_role, reason=f"Muted by {ctx.author} for {minutes} minutes")
    await ctx.send(f"🔇 {member.mention} muted for {minutes} minute(s).")
    await asyncio.sleep(max(1, minutes) * 60)
    if mute_role in member.roles:
        await member.remove_roles(mute_role, reason="Mute duration ended")
        await ctx.send(f"🔊 {member.mention} unmuted.")

@bot.command(help="Set a reminder. Usage: !remindme <minutes> <what>")
async def remindme(ctx: commands.Context, minutes: int, *, task: str):
    remind_time = datetime.utcnow() + timedelta(minutes=minutes)
    reminders[ctx.author.id] = (remind_time, task)
    await ctx.send(f"⏰ Reminder set for {minutes} minute(s): **{task}**")
    await asyncio.sleep(minutes * 60)
    await ctx.send(f"⏰ Hey {ctx.author.mention}, reminder: **{task}**")

@bot.command(help="Say hello")
async def hello(ctx: commands.Context):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command(help="Basic server info")
async def serverinfo(ctx: commands.Context):
    g = ctx.guild
    embed = discord.Embed(title=g.name, description="Server Info", color=0x00ff00)
    embed.add_field(name="Members", value=g.member_count)
    embed.add_field(name="Owner", value=str(g.owner))
    embed.add_field(name="Created", value=g.created_at.strftime("%Y-%m-%d"))
    await ctx.send(embed=embed)

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN in .env")
bot.run(TOKEN)
