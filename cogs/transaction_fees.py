"""transactions fees commands"""
import json

import aiohttp
import discord
from discord.ext import commands

from logs.logger import logger
from src.utils import sendAdEmbed

with open("config.json", encoding="utf-8") as file:
    config = json.load(file)


class TransactionFees(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ETHSCAN_API = config["ETHSCAN_API"]
        self.BSCSCAN_API = config["BSCSCAN_API"]
        self.POLYGONSCAN_API = config["POLYGONSCAN_API"]

    @discord.app_commands.command(name="gas",
                                  description="⛽ Get Ethereum gas fees ⛽")
    async def gas(self, interaction: discord.Interaction):
        try:
            # ------------------------------------------
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={self.ETHSCAN_API}") as r:
                    fees_response = await (r.json())

            fast = round(float(fees_response["result"]["FastGasPrice"]))
            standard = round(float(fees_response["result"]["ProposeGasPrice"]))
            slow = round(float(fees_response["result"]["SafeGasPrice"]))
            average = round(float(fees_response["result"]["suggestBaseFee"]))
            # ------------------------------------------

            embed = discord.Embed(title=":fuelpump: Ethereum Gas", color=0x5872a0)
            embed.set_thumbnail(url="https://ethgasstation.info/static/images/egs_transparent.png")
            embed.add_field(name=":comet:  **Fast**  :comet:", value=f"{fast} Gwei | 15 sec", inline=False)
            embed.add_field(name=":dizzy:  **Standar**  :dizzy:", value=f"{standard} Gwei | 1 min", inline=False)
            embed.add_field(name=":turtle:  **Slow**  :turtle:", value=f"{slow} Gwei | 3 mins", inline=False)
            embed.add_field(name=":snail:  **Average**  :snail:", value=f"{average} Gwei | 3 mins", inline=False)
            # embed.set_footer(text="Test")
            # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Test"))
            # ------------------------------------------------
            try:
                await sendAdEmbed(self, interaction, embed)
            except Exception as e:
                logger.info(f"Failed to send gas fees embed: {e}")
            # ---------------------------------------------
        except Exception as e:
            logger.info(f"Failed to get gas fees: {e}")

    @discord.app_commands.command(name="btcfee",
                                  description="⛏️ Get Bitcoin network fees ⛏️")
    async def btcfee(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://mempool.space/api/v1/fees/recommended") as r:
                    btc_response = await (r.json())
            # ------------------------------------------
            rapid = btc_response["fastestFee"]
            fast = btc_response["halfHourFee"]
            standar = btc_response["hourFee"]
            slow = btc_response["minimumFee"]
            # ------------------------------------------
            embed = discord.Embed(title=":pick: Bitcoin Fees", color=0xf77e33)
            embed.set_thumbnail(url="https://www.cryptocompare.com/media/37746251/btc.png?width=200")
            embed.add_field(name=":comet:  **Rapid**  :comet:", value=f"{rapid} sat/vB | ~10 mins", inline=False)
            embed.add_field(name=":dizzy:  **Fast**  :dizzy:", value=f"{fast} sat/vB | ~30 mins", inline=False)
            embed.add_field(name=":turtle:  **Standar**  :turtle:", value=f"{standar} sat/vB | ~60 mins", inline=False)
            embed.add_field(name=":snail:  **Minimum Fee**  :snail:", value=f"{slow} sat/vB | >60 mins", inline=False)
            # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" BTC fees"))
            # ------------------------------------------------
            try:
                await sendAdEmbed(self, interaction, embed)
            except Exception as e:
                logger.exception(f"Failed to send btc fees embed: {e}")
            # ---------------------------------------------
        except Exception as e:
            logger.exception(f"Failed to get btc fees: {e}")

    @discord.app_commands.command(name="bscgas",
                                  description="⛽ Binance Smart Chain gas fees ⛽")
    async def bscgas(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.bscscan.com/api?module=gastracker&action=gasoracle&apikey={self.BSCSCAN_API}") as r:
                    fees_response = await (r.json())
            # ------------------------------------------
            fast = round(float(fees_response["result"]["FastGasPrice"]))
            standard = round(float(fees_response["result"]["ProposeGasPrice"]))
            slow = round(float(fees_response["result"]["SafeGasPrice"]))
            # ------------------------------------------
            embed = discord.Embed(title=":fuelpump: BSC Gas", color=0xedad0e)
            embed.set_thumbnail(
                url="https://user-images.githubusercontent.com/7338312/127578976-d47069cb-c162-4ab5-ad73-be17b2c1796d.png")
            embed.add_field(name=":comet:  **Rapid**  :comet:", value=f"{fast} Gwei | 15 sec", inline=False)
            embed.add_field(name=":dizzy:  **Fast**  :dizzy:", value=f"{standard} Gwei | 1 min", inline=False)
            embed.add_field(name=":turtle:  **Standar**  :turtle:", value=f"{slow} Gwei | 3 mins", inline=False)
            try:
                await sendAdEmbed(self, interaction, embed)
            except Exception as e:
                logger.exception(f"Failed to send bsc gas embed: {e}")
            # ---------------------------------------------
            # await donationMensage(ctx)
        except Exception as e:
            logger.exception(f"Failed to get bsc gas: {e}")

    @discord.app_commands.command(name="polygas",
                                  description="⛽ Polygon network gas fees ⛽")
    async def polygas(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.polygonscan.com/api?module=gastracker&action=gasoracle"
                                       f"&apikey={self.POLYGONSCAN_API}") as r:
                    fees_response = await (r.json())
            # ------------------------------------------
            fast = round(float(fees_response["result"]["FastGasPrice"]))
            standard = round(float(fees_response["result"]["ProposeGasPrice"]))
            slow = round(float(fees_response["result"]["SafeGasPrice"]))
            average = round(float(fees_response["result"]["suggestBaseFee"]))
            # ------------------------------------------
            embed = discord.Embed(title=":fuelpump: Polygon Gas", color=0x6900ea)
            embed.set_thumbnail(
                url="https://user-images.githubusercontent.com/7338312/127578967-a7097067-9b0a-44d2-baf6-e3541a511c70"
                    ".png")
            embed.add_field(name=":comet:  **Rapid**  :comet:", value=f"{fast} Gwei | ASAP",
                            inline=False)
            embed.add_field(name=":dizzy:  **Fast**  :dizzy:", value=f"{standard} Gwei | < 30s", inline=False)
            embed.add_field(name=":turtle:  **Standar**  :turtle:", value=f"{slow} Gwei | 3 mins",
                            inline=False)
            embed.add_field(name=":snail:  **Slow**  :snail:", value=f"{average} Gwei | >10 mins",
                            inline=False)
            try:
                await sendAdEmbed(self, interaction, embed)
            except Exception as e:
                logger.exception(f"Failed to send poly gas embed: {e}")
            # ---------------------------------------------
        except Exception as e:
            logger.exception(f"Failed to get polygon gas: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        TransactionFees(bot)
    )
