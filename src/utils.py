"""Contains unrelated bot functions used in ``cogs/`` """
import random

import aiohttp
import discord
import requests

from logs.logger import logger
from cryptobot import config

promo_phrases = [
    "Unlock CryptoBot premium",
    "Join CryptoBot Community"]
bot_status = ["Unlock CryptoBot premium", "Checking the blockchain", "Join CryptoBot Official Channel",
              "Use: /donate for support CryptoBot"]


def get_promo() -> str:
    """Get a random promo phrases."""
    return random.choice(promo_phrases)


def get_bot_status() -> str:
    """Get a random status for the bot."""
    return random.choice(bot_status)


def get_tor_session():
    logger.info("starting tor session")
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:' + config["TOR_PORT"],
                       'https': 'socks5h://127.0.0.1:' + config["TOR_PORT"]}
    return session


async def delete_price_alert_by_id(alert_id, url: str):
    try:
        async with aiohttp.ClientSession() as session:
            await session.delete(f"{url}", data=f"{alert_id}")
    except Exception as e:
        logger.exception(f"Error deleting price alert {e}")


async def sendAdEmbed(self, interaction: discord.Interaction, embed):
    try:
        ad_embed = discord.Embed(title=get_promo(), url="https://discord.gg/nNRKgYkvj9",
                                 color=0xf90206)
        embed.set_footer(text=get_promo(), icon_url=self.bot.user.avatar)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name=f"{get_bot_status()}"))
        return await interaction.response.send_message(embeds=[ad_embed, embed])
    except Exception:
        return await interaction.response.send_message(embed=embed)
