"""miscellaneous commands."""

import discord
import psutil
from discord import app_commands
from discord.ext import commands, tasks

from logs.logger import logger
from src.utils import get_bot_status, sendAdEmbed


class Misc(commands.Cog):
    """Misc commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.change_status.start()

    # end def

    @tasks.loop(minutes=5)
    async def change_status(self):
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name=f"{get_bot_status()}"))

    @change_status.before_loop
    async def before_change_status(self):
        logger.info("Change status waiting to the bot to be ready")
        await self.bot.wait_until_ready()
        logger.info("Change status loop started")

    ####################################################################################################################
    @app_commands.command(name="info", description="ℹ️ Get bot info ℹ️")
    async def info(self, interaction: discord.Interaction):
        try:
            servers = len(self.bot.guilds)

            members = 0
            for guild in self.bot.guilds:
                members += guild.member_count

            channels = 0
            for guild in self.bot.guilds:
                for text_channels in guild.text_channels:
                    channels += 1

            embed = discord.Embed(title=":information_source: __**BOT INFORMATION**__ :information_source:")
            embed.add_field(name=":earth_americas: **Servers** :earth_americas:", value=f"Serving {servers} servers",
                            inline=False)
            embed.add_field(name=":busts_in_silhouette: **Used by**:busts_in_silhouette: ",
                            value=f"Serving {members} people", inline=False)
            embed.add_field(name=":satellite: **Channels** :satellite:", value=f"{channels}", inline=False)
            embed.add_field(name=":gear: **Version** :gear:", value=f"{self.bot.version}", inline=False)
            # embed.add_field(name=":green_square: **Shard ID** :green_square:", value=f"{self.bot.shard_id}",
            #                inline=True)
            # embed.add_field(name=":green_square: **Shard Count** :green_square:", value=f"{self.bot.shard_count}",
            #                 inline=True)
            embed.add_field(name=":bar_chart: **Server Usage** :bar_chart:",
                            value=f"CPU: {psutil.cpu_percent()}% RAM: {psutil.virtual_memory()[2]}%", inline=False)
            try:
                await sendAdEmbed(self, interaction, embed)
            except Exception as e:
                logger.exception(f"Failed to send info embed: {e}")
        except Exception as e:
            logger.exception(f"Failed to send info command: {e}")

    @app_commands.command(name="inviteme", description="🌐 Invite me to your server 🌐")
    async def inviteme(self, interaction: discord.Interaction):
        embed = discord.Embed(title=":star2: __**INVITE ME**__ :star2:",
                              url="https://top.gg/bot/860134458308821042/invite",
                              color=0xf77e33)
        try:
            await sendAdEmbed(self, interaction, embed)
        except Exception as e:
            logger.exception(f"Failed to send invite me embed: {e}")

    @app_commands.command(name="vote", description="💫 Vote for me on top.gg 💫")
    async def vote(self, interaction: discord.Interaction):
        embed = discord.Embed(title=":partying_face:__**VOTE ME**__ :partying_face:",
                              url="https://top.gg/bot/860134458308821042/vote", color=0xf77e33)
        try:
            await sendAdEmbed(self, interaction, embed)
        except Exception as e:
            logger.exception(f"Failed to send vote embed: {e}")

    @app_commands.command(name="support", description="❓ Discord support server ❓")
    async def support(self, interaction: discord.Interaction):
        embed = discord.Embed(title=":robot:__**JOIN SUPPORT DISCORD CHANNEL**__ :robot:",
                              url="https://discord.gg/nNRKgYkvj9", color=0xf77e33)
        try:
            await sendAdEmbed(self, interaction, embed)
        except Exception as e:
            logger.exception(f"Failed to send support embed: {e}")

    @app_commands.command(name="help",
                          description="help command")
    async def help_command(self, interaction: discord.Interaction):
        try:
            crypto = "\n`/price {CRYPTO}` => See cryptocurrency price. \nMore than 5000 assets!!."
            bitcoin = (
                "\n`/wallet_info {BTC_ADDRESS}` => Saw transactions of a bitcoin address in chain. This means you can "
                "only see confirmed transactions.\n`/check_transaction {TRANSACTION HASH}` => returns the status of "
                "the transaction given a transaction hash.\n`/post_transaction {TX}` => post raw transaction to "
                "bitcoin network. You need a signed transaction to post it.")
            fees = (
                "\n`/gas` => Shows ETH GAS price.\n`/btcfee` => Shows Bitcoin fees.\n`/bscgas` => Shows Binance Smart "
                "Chain gas.\n`/polygas` => Shows Polygon gas.")
            robosats = ("\n`/robosats_offers {FIAT} {DIRECTION}`=> Returns all active offers given a fiat currency "
                        "and the purpose of the order\n "
                        "`/create_robosats_alert {FIAT} {AMOUNT} {PREMIUM} {METHOD} {DIRECTION}`=> Create a alert for "
                        "robosats exchange\n "
                        "`/my_robosats_alerts`=> Show your robosats active alerts\n "
                        "`/remove_robosats_alert {ALERT_ID}`=> Remove your robosats alert\n")
            misc = (
                "\n`/inviteme` => Invite CryptoBot to your server.\n `/vote` => give us 5 stars on top.gg.\n "
                "`/support` => Join if you find a bug or if you have some suggestions.\n `/info` => Bot info and some "
                "stats.\n `/server_info` => Get the active functions on your server.")
            donations = "\n`/donate` => Invite me a coffee."

            embed = discord.Embed(title="__**COMMAND LIST**__", color=0xf77e33)
            embed.add_field(name=":dollar:  Crypto Price  :dollar:", value=crypto, inline=False)
            embed.add_field(name=":pick:  Transaction Fees  :pick:", value=fees, inline=False)
            embed.add_field(name=":coin:  Bitcoin  :coin:", value=bitcoin, inline=False)
            embed.add_field(name=":robot: Robosats :robot:", value=robosats, inline=False)
            embed.add_field(name=":balloon:  Misc  :balloon:", value=misc, inline=False)
            embed.add_field(name=":sparkling_heart:  Donations  :sparkling_heart:", value=donations, inline=False)

            await sendAdEmbed(self, interaction, embed)
        except Exception as e:
            logger.exception(f"{interaction.user.name} tried to get help command  but failed.\n{e}")

    @app_commands.command(name="donate",
                          description="Donate to cryptobot project")
    async def donate(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title=":heartpulse: __**DONATIONS**__ :heartpulse:")
            embed.add_field(name="BTC", value=f"bc1qdgpwwl3wwlmmyerl73xyz3c8rqa75yxwm3tzzr", inline=False)
            embed.add_field(name="ETH", value=f"0xE3d17F552F36aCBb5f1F8010e4F9D5F683a8e117", inline=False)
            embed.add_field(name="USDT (ERC20)", value=f"0xE3d17F552F36aCBb5f1F8010e4F9D5F683a8e117", inline=False)
            try:
                await sendAdEmbed(self, interaction, embed)
            except Exception as e:
                logger.exception(f"Error on donate: {e}")
                await interaction.response.send_message(embed=embed)
            # ---------------------------------------------
            await self.bot.change_presence(status=discord.Status.online,
                                           activity=discord.Game(f'Use: /donate for support me'))
        except Exception as e:
            logger.exception(f"Error on donate: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Misc(bot)
    )
