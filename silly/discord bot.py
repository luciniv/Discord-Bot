TOKEN = "MTIwODU5MTY1MDc2Nzc2OTY1MA.GOItwt.eRXODQOcQcQyl9v0WMxPnzNTMfsoP1pICsQJxA"

import discord
from discord.ext import commands
from discord import app_commands

description = '''testing bot'''

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

#1208482410304376843

class BanFlags(commands.FlagConverter):
    user: discord.Member = commands.flag(description='The user to ban')
    reason: str = commands.flag(description='The reason for the ban')

class KickFlags(commands.FlagConverter):
    user: discord.Member = commands.flag(description='The user to kick')
    reason: str = commands.flag(description='The reason for the kick', default="No reason given")

class RoleFlags(commands.FlagConverter):
    user: discord.Member = commands.flag(description='The user to role')
    role: discord.Role = commands.flag(description='The desired role to give / remove')
    remove: bool = commands.flag(description='Set this value to TRUE to remove the role', default = False)

class MyButton(discord.ui.Button):
    def __init__(self, *, style: discord.ButtonStyle, label: str, custom_id: str):
        super().__init__(style=style, label=label, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        print(f'user: {interaction.user}')
        #await interaction.response.send_message("You pressed the button")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("ready!")

@bot.event
async def on_message(message):
    if "hello" in message.content.lower():
        await message.channel.send(f"shrimp <@{message.author.id}>")
    await bot.process_commands(message)

@bot.hybrid_command(name="ping", with_app_command=True, description="Pongs you back!")
async def ping(ctx):
    await ctx.send("pong")

@bot.hybrid_command(name="members", with_app_command=True, description="Returns server member count")
async def members(ctx):
    true_member_count = len([m for m in ctx.guild.members if not m.bot])
    await ctx.send(f"current members (excluding bots): {true_member_count}")

@bot.hybrid_command(name="kick", with_app_command=True, description="Kick a user")
async def kick(ctx, *, flags: KickFlags):
    embed=discord.Embed(title="Member Kicked",  
                        description=f"Successfully kicked <@{flags.user.id}> **Reason**: {flags.reason}",
                        color=0x57F287)
    await flags.user.kick(reason=flags.reason)
    await ctx.send(embed=embed)

@bot.hybrid_command(name="ban", with_app_command=True, description="Ban a user")
async def ban(ctx, *, flags: BanFlags):
    embed=discord.Embed(title="Member Banned",  
                        description=f"Successfully banned {flags.user} | **Reason**: {flags.reason}",
                        color=0x57F287)
    await flags.user.ban(reason=flags.reason)
    await ctx.send(embed=embed)

@bot.hybrid_command(name="manage_roles", with_app_command=True, description="Manage a user's roles")
async def manage_roles(ctx, *, flags: RoleFlags): 
    user = flags.user
    role = flags.role
    embedGiveSuccess=discord.Embed(title="Role Given",  
                        description=f"Gave the role <@&{role.id}> to <@{user.id}>",
                        color=0x57F287)
    embedGiveFail=discord.Embed(title="Unable to Give Role",  
                        description=f"<@{user.id}> already has the role <@&{role.id}>",
                        color=0xED4245)
    embedRemoveSuccess=discord.Embed(title="Role Removed",  
                        description=f"Removed the role <@&{role.id}> from <@{user.id}>",
                        color=0x57F287)
    embedRemoveFail=discord.Embed(title="Unable to Remove Role",  
                        description=f"<@{user.id}> did not have the role <@&{role.id}>",
                        color=0xED4245)
    
    if flags.remove == False:
        if role in user.roles:
            await ctx.send(embed=embedGiveFail)
        else:
            await user.add_roles(role)
            await ctx.send(embed=embedGiveSuccess)
    else:
        if role not in user.roles:
            await ctx.send(embed=embedRemoveFail)
        else:
            await user.remove_roles(role)
            await ctx.send(embed=embedRemoveSuccess)

@bot.hybrid_command(title="send_button")
async def send_button(ctx):
    button = MyButton(style=discord.ButtonStyle.blurple, label="Click me!", custom_id="button_click")
    view = discord.ui.View()
    view.add_item(button)
    await ctx.send("Press the button below:", view=view)

@bot.event
async def on_button_click(interaction: discord.Interaction):
    if interaction.custom_id == "button_click":
        await interaction.reply("You pressed the button")

#@bot.tree.command()
#async def hi(interaction: discord.Interaction):
    #await interaction.response.send_message(f"hi {interaction.user.mention}!", ephemeral=True)

bot.run(TOKEN)

