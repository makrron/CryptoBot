"""Contains unrelated bot functions used in ``cogs/`` """
import random

import aiohttp
import discord
import requests
from urllib3 import Retry

from logs.logger import logger
from requests.adapters import HTTPAdapter
from cryptobot import config


promo_phrases = ["Use: /donate for support CryptoBot", "Use Robosats: Simple and private LN P2P exchange", "Buy non-KYC sats now this TOR Browser"]
bot_status = ["Unlock CryptoBot premium", "Checking the blockchain", "Join CryptoBot Official Channel",
              "Use: /donate for support CryptoBot, "]


def get_promo() -> str:
    """Get a random promo phrases."""
    return random.choice(promo_phrases)


def get_bot_status() -> str:
    """Get a random status for the bot."""
    return random.choice(bot_status)


def get_tor_session():
    logger.info("starting tor session")
    session = requests.session()

    # configurar el adaptador de reintentos
    retries = Retry(total=15, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries, pool_connections=100, pool_maxsize=100)

    # añadir el adaptador a la sesión
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # configurar los proxies para tor
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
        ad_embed = discord.Embed(title=get_promo(), url="https://learn.robosats.com",
                                 color=0xf90206, )
        embed.set_footer(text=get_promo(), icon_url=self.bot.user.avatar)
        embed.set_image(url="https://a.fsdn.com/con/app/proj/robosats.s/screenshots/robosats2.jpeg/1000/auto/1")
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name=f"{get_bot_status()}"))
        return await interaction.response.send_message(embeds=[ad_embed, embed])
    except Exception:
        return await interaction.response.send_message(embed=embed)
