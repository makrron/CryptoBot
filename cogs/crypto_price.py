import json

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from logs.logger import logger
from src.utils import sendAdEmbed

with open("config.json", encoding="utf-8") as file:
    config = json.load(file)


class CryptoPrice(commands.Cog):
    """Price of cryptocurrencies"""

    def __init__(self, bot: commands.Bot):
        self.CCAPI = config["CCAPI"]
        self.bot = bot

    ####################################################################################################################

    @app_commands.command(name="price",
                          description="💲 See cryptocurrency price 💲")
    @app_commands.describe(crypto_currency_symbol="Symbol of the crypto currency you want to check")
    async def price(self, interaction: discord.Interaction, crypto_currency_symbol: str):
        try:
            crypto_currency_symbol = crypto_currency_symbol.upper()
            asset_URL = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + crypto_currency_symbol + "&tsyms=USD,EUR&api_key=" + self.CCAPI

            # ------------------------------------------
            async with aiohttp.ClientSession() as session:
                async with session.get(asset_URL) as r:
                    if r.status == 200:
                        asset_response = await r.json()
                    else:
                        await interaction.response.send_message(
                            f"```{r.status} {r.reason}```")
                        return
            # ------------------------------------------
            if not "Response" in asset_response:
                market_response = asset_response["RAW"][crypto_currency_symbol]["USD"]["MARKET"]
                usd_value = asset_response["DISPLAY"][crypto_currency_symbol]["USD"]["PRICE"]
                eur_value = asset_response["DISPLAY"][crypto_currency_symbol]["EUR"]["PRICE"]
                change_usd = asset_response["DISPLAY"][crypto_currency_symbol]["USD"]["CHANGEPCT24HOUR"]
                change_eur = asset_response["DISPLAY"][crypto_currency_symbol]["EUR"]["CHANGEPCT24HOUR"]

                if (float(change_eur) >= 0.0) & (float(change_usd) >= 0.0):
                    icon = ":arrow_upper_right:"
                else:
                    icon = ":arrow_lower_right:"

                imageURL = asset_response["DISPLAY"][crypto_currency_symbol]["USD"]["IMAGEURL"]
                imageURL = "https://cryptocompare.com/" + imageURL

                embed = discord.Embed(color=0xefa802)
                embed.set_author(name=f"{crypto_currency_symbol.upper()}", icon_url=imageURL)
                # embed.set_thumbnail(url="https://cryptocompare.com/" + imageURL)
                embed.add_field(name=":dollar: Dollar Price :dollar:", value=usd_value, inline=True)
                embed.add_field(name=f"{icon} 24H Change {icon}", value=f"{change_usd}%", inline=True)
                embed.add_field(name="Market", value=f"{market_response}", inline=False)
                embed.add_field(name=":euro: Euro Price :euro:", value=eur_value, inline=True)
                embed.add_field(name=f"{icon} 24H Change {icon}", value=f"{change_eur}%", inline=True)
                # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                # name=f"{asset.upper()} price"))

                try:
                    await sendAdEmbed(self, interaction, embed)
                except Exception as e:
                    logger.exception(f"Failed to send price embed: {e}")
            else:
                await interaction.response.send_message("```Error: " + crypto_currency_symbol.upper()
                                                        + " is not a valid cryptocurrency```")
        except Exception as e:
            logger.exception(f"Failed to get price: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        CryptoPrice(bot)
    )
