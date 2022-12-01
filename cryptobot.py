"""Main file, intended to be launched."""

__version__ = "6.1.0"

import json

import aiohttp
import discord
from discord.ext import commands

from logs.logger import logger

# Configuration.
with open("config.json", encoding="utf-8") as file:
    config = json.load(file)


class AutoShardedBot(commands.Bot):
    """Encapsulate a discord bot."""

    def __init__(self):
        intents = discord.Intents.default()
        # intents.members = True
        intents.guilds = True
        self.version = __version__
        self.chunk_at_startup = False

        super().__init__(config["PREFIX"],
                         token=config["TOKEN"],
                         description="CryptoBot - A bot for crypto related stuff",
                         intents=intents,
                         application_id=config["APPLICATION_ID"])

    async def on_ready(self):
        """Log information about bot launching."""
        logger.info("Bot %s connected on %s servers",
                    self.user.name,
                    len(self.guilds))

    async def setup_hook(self):
        """Load and sync app commands."""
        await self.load_extension("cogs.crypto_price")
        await self.load_extension("cogs.misc")
        await self.load_extension("cogs.bitcoin")
        await self.load_extension("cogs.transaction_fees")
        await self.load_extension("cogs.robosats_alerts")
        await self.tree.sync()

    async def on_guild_join(self, guild):
        logger.info(f"Bot join: {guild.name}")
        servers = len(self.guilds)
        url = "https://top.gg/api/bots/860134458308821042/stats"
        obj = {'server_count': servers}
        header = {
            "Authorization": config["TOPGG_AUTH"]
        }

        async with aiohttp.ClientSession() as session:
            await session.post(url, headers=header, data=obj)

        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game(f'/help | Serving {servers} servers'))

    async def on_guild_remove(self, guild):
        logger.info(f"Bot leave: {guild.name}")
        servers = len(self.guilds)
        url = "https://top.gg/api/bots/860134458308821042/stats"
        obj = {'server_count': servers}
        header = {
            "Authorization": config["TOPGG_AUTH"]
        }

        async with aiohttp.ClientSession() as session:
            await session.post(url, headers=header, data=obj)

        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game(f'/help | Serving {servers} servers'))

    async def on_command_error(self, ctx, error):
        """Log errors."""
        logger.error(f"{ctx.message.author} in {ctx.message.guild}", exc_info=error)
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send("```CryptoBot is now using SLASH COMMANDS```\n```Type /help for check all new commands```")
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("```" + str(error) + "```"
                           + "```type -help if you don´t know how this bot works```")
        if isinstance(error, commands.BadArgument):
            await ctx.send("```" + str(error) + "```"
                           + "```type -help if you don´t know how this bot works```")


if __name__ == "__main__":
    cryptobot = AutoShardedBot()
    cryptobot.run(config["TOKEN"])
