"""bitcoin related commands"""
import os

import aiohttp
import discord
import requests
from discord import app_commands
from discord.ext import commands

from logs.logger import logger
from src.utils import sendAdEmbed


class Bitcoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="wallet_info",
                          description="🪙 Saw info of a bitcoin wallet.  🪙")
    @discord.app_commands.describe(wallet="The wallet you want to check")
    async def bitcoinwalletinfo(self, interaction: discord.Interaction, wallet: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://mempool.space/api/address/' + wallet) as r:
                    if r.status == 200:
                        response = await r.json()

                        transaction_received_count = response["chain_stats"]["funded_txo_count"]
                        amount_received = response["chain_stats"]["funded_txo_sum"]
                        transaction_send_count = response["chain_stats"]["spent_txo_count"]
                        amount_send = response["chain_stats"]["spent_txo_sum"]

                        embed = discord.Embed(title=wallet.upper(), color=0xefa802)
                        embed.set_thumbnail(url="https://www.cryptocompare.com/media/37746251/btc.png?width=200")
                        embed.add_field(name="Transactions received:", value=f"{transaction_received_count}",
                                        inline=False)
                        embed.add_field(name="Transactions send:", value=f"{transaction_send_count}", inline=False)
                        embed.add_field(name="Amount Received:", value=f"{round(amount_received * 0.00000001, 8)} BTC",
                                        inline=False)
                        embed.add_field(name="Amount Send:", value=f"{round(amount_send * 0.00000001, 8)} BTC",
                                        inline=False)
                        embed.add_field(name="Total Balance:",
                                        value=f"{round(amount_received * 0.00000001 - amount_send * 0.00000001, 8)} BTC",
                                        inline=False)
                        # ------------------------------------------------
                        try:
                            await sendAdEmbed(self, interaction, embed)
                        except Exception as e:
                            logger.exception(f"Error sending bitcoin wallet info embed: {e}")
                        # ---------------------------------------------
                    elif r.status == 400:
                        await interaction.response.send_message("```ERROR: INVALID BTC ADDRESS```")
        except Exception as e:
            logger.exception(f"Error getting bitcoin wallet info: {e}")

    @app_commands.command(name="check_transaction",
                          description="✅ Check the status of your bitcoin transaction ✅")
    @app_commands.describe(transaction_hash="Bitcoin transaction hash code")
    async def checktransaction(self, interaction: discord.Interaction, transaction_hash: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://mempool.space/api/tx/' + transaction_hash + '/status') as r:
                    if r.status == 200:
                        response = await r.json()

                        confirmed = response["confirmed"]
                        if confirmed:
                            embed = discord.Embed(title='Transaction confirmed'.upper(), color=0x5bea02)
                            try:
                                await sendAdEmbed(self, interaction, embed)
                            except Exception as e:
                                logger.exception(f"Error sending transaction confirmed embed: {e}")
                        else:
                            embed = discord.Embed(title='Transaction unconfirmed'.upper(), color=0xfc1d05)
                            # ------------------------------------------------
                            try:
                                await sendAdEmbed(self, interaction, embed)
                            except Exception as e:
                                logger.exception(f"Error sending transaction unconfirmed embed: {e}")
                            # ---------------------------------------------
                    elif r.status == 400:
                        await interaction.response.send_message("```ERROR: INVALID BTC TRANSACTION```")
        except Exception as e:
            logger.exception(f"Error getting bitcoin transaction info: {e}")

    @app_commands.command(name="post_transaction",
                          description="📄 Post your offline transaction to the Bitcoin network. 📄")
    @app_commands.describe(transaction_hash="Bitcoin transaction hash code")
    async def post_transaction(self, interaction: discord.Interaction, transaction_hash: str):
        try:
            link = "https://mempool.space/api/tx"

            await interaction.response.send_message("```TOR IS STARTING...```")
            if os.system("service tor start") == 0:
                await interaction.edit_original_response(content="```SUCCESSFULLY STARTED TOR```")

                with requests.Session() as s:
                    # require pip install PySocks
                    s.proxies = {'http': 'socks5h://127.0.0.1:9050/', 'https': 'socks5h://127.0.0.1:9050/'}

                    response = s.get("http://httpbin.org/ip").json()

                    await interaction.edit_original_response(content=f"TOR IP: {response['origin']}")

                    post = requests.post(link, data=transaction_hash)

                    if post.status_code == 200:
                        embed = discord.Embed(title=":white_check_mark:", color=0x5bea02)
                        embed.set_author(name=f"TRANSACTION SEND")
                        embed.add_field(name="Your transaction id:", value=f"{post.text}", inline=False)
                        await sendAdEmbed(self, interaction, embed)
                    else:
                        error = post.text.split('"message":"')
                        error = error[1][:-2]
                        embed = discord.Embed(title=":x:", color=0xbc1616)
                        embed.set_author(name=' TRANSACTION FAILED')
                        embed.add_field(name="Error:", value=f"{error}", inline=False)
                        await sendAdEmbed(self, interaction, embed)

                await interaction.edit_original_response(content="```TOR IS STOPPING...```")
                if os.system("service tor stop") == 0:
                    await interaction.edit_original_response(content="```SUCCESSFULLY STOPPED TOR```")
                else:
                    await interaction.edit_original_response(content="```TOR STOPPING PROCESS FAILED```")
            else:
                await interaction.edit_original_response(content="```TOR NOT RUNNING```\n`Aborting process`")
        except Exception as e:
            await interaction.edit_original_response(content=f"Error {e}")
            logger.exception(f"Error posting bitcoin transaction: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Bitcoin(bot)
    )
