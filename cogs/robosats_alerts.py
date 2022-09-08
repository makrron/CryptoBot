import collections
import json

import aiohttp
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks

from logs.logger import logger
from src.exchanges.robosats import Robosats
from src.utils import get_tor_session, delete_price_alert_by_id


class RoboSatsAlerts(commands.Cog):
    """Robosats alerts"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.robosatsAlertTask.start()
        self.referral_link_onion = "http://robosats6tkf3eva7x2voqso3a5wcorsnw34jveyxfqi2fu7oyheasid.onion/ref/nHcL" \
                                   "-8ye_Yo "
        self.icon_url = "https://github.com/Reckless-Satoshi/robosats/blob/7083423189063995e15a904e9738dce1292c3773" \
                        "/frontend/static/assets/images/favicon-32x32.png?raw=true "

    ####################################################################################################################

    @tasks.loop(minutes=2)
    async def robosatsAlertTask(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://127.0.0.1:5000/robosats_alerts") as r:
                    if r.status == 200:
                        response = await r.json()
                        if len(response['ALERTS']) > 0:  # if database is empty don't do this
                            tor_session = get_tor_session()

                            for item in response['ALERTS']:
                                alert_id = item['ALERT_ID']
                                user_id = item['USER_ID']
                                fiat_currency = item['FIAT_CURRENCY']
                                amount = item['AMOUNT']
                                premium = item['PREMIUM']
                                method = item['METHOD']
                                direction = item['DIRECTION']

                                if direction == "sell":
                                    offers = Robosats.getOffers(fiat_currency, "buy", tor_session)
                                else:
                                    offers = Robosats.getOffers(fiat_currency, "sell", tor_session)
                                for offer in offers:
                                    if (offer["dif"] == float(premium)) and \
                                            (float(offer['min_amount']) <= float(amount) or float(amount) <= float(
                                                offer['max_amount'])) and \
                                            ((offer['method']).upper() in method.upper() or method.upper() in (
                                                    offer['method']).upper()):
                                        user = await self.bot.fetch_user(int(user_id))
                                        embed = discord.Embed(title=":warning: __**ROBOSATS ORDER ALERT**__ :warning:",
                                                              url=self.referral_link_onion)
                                        embed.add_field(name=f"A order with your requisites was found",
                                                        value=f"· You will {direction} BTC for {fiat_currency} \n "
                                                              f"· Amount: {amount} {fiat_currency} \n "
                                                              f"· Payment method: {method.upper()}",
                                                        inline=False)
                                        embed.set_footer(text="Powered by Robosats", icon_url=self.icon_url)

                                        await user.send(embed=embed)
                                        await delete_price_alert_by_id(alert_id,
                                                                       f"http://127.0.0.1:5000/robosats_alerts/{user_id}/")
                                        break
        except Exception as e:
            logger.exception(f"Error on robosatsAlertTask: {e}")

    @robosatsAlertTask.before_loop
    async def before_robosatsAlertTask(self):
        logger.info("robosatsAlertTask waiting to the bot to be ready.")
        await self.bot.wait_until_ready()
        logger.info("robosatsAlertTask started.")

    # ###################################################################################################################
    @app_commands.command(name="robosats_offers",
                          description="📒 Returns all active offers given a fiat currency and the purpose of the "
                                      "order 📒")
    @app_commands.describe(fiat="Fiat currency",
                           direction="You want to?")
    @app_commands.choices(direction=[
        Choice(name="buy", value="sell"),
        Choice(name="sell", value="buy")])
    async def offers(self, interaction: discord.Interaction, fiat: str, direction: Choice[str]):
        try:
            offers = Robosats.getOffers(fiat, direction.value, get_tor_session())
            if direction.value == "buy":
                embed_response = discord.Embed(
                    title=f":information_source: **BUYING** BTC for {fiat.upper()} :information_source:",
                    url=self.referral_link_onion)
            else:
                embed_response = discord.Embed(
                    title=f":information_source: **SELLING** BTC for {fiat.upper()} :information_source:",
                    url=self.referral_link_onion)
            for offer in offers:
                # print(offer)
                embed_response.add_field(name=f"Methods: {offer['method']}",
                                         value=f"· Min amount: {offer['min_amount']}\n"
                                               f"· Max amount: {offer['max_amount']}\n"
                                               f"· Premium: {offer['dif']}%",
                                         inline=False)
            embed_response.set_footer(text="Powered by Robosats",
                                      icon_url=self.icon_url)
            await interaction.response.send_message(embed=embed_response)
        except Exception as e:
            logger.exception(f"Error checking offers: {e}")

    @app_commands.command(name="create_robosats_alert",
                          description="🔔 Create a alert for robosats exchange 🔔")
    @app_commands.describe(fiat="Fiat currency symbol. Ex: usd",
                           amount="Amount of fiat you want to spend",
                           premium="Percentage of premium you want to set",
                           method="Introduce one or more payments methods separated with a space",
                           direction="What do you want to do?")
    @app_commands.choices(direction=[Choice(name="buy", value="buy"),
                                     Choice(name="sell", value="sell")])
    async def create_alert(self, interaction: discord.Interaction, fiat: str, amount: str, premium: str, method: str,
                           direction: Choice[str]):
        try:
            user_id = interaction.user.id
            objects_list = {"ALERTS": []}
            d = collections.OrderedDict()
            d["USER_ID"] = user_id
            d["FIAT_CURRENCY"] = fiat.upper()
            d["AMOUNT"] = amount
            d["PREMIUM"] = premium
            d["METHOD"] = method
            d["DIRECTION"] = direction.value
            objects_list["ALERTS"].append(d)

            async with aiohttp.ClientSession() as session:
                async with session.post(f"http://127.0.0.1:5000/robosats_alerts/{user_id}/",
                                        json=json.dumps(objects_list)) as r:
                    if r.status == 200:
                        await interaction.response.send_message("```Your alert was created ```")
        except Exception as e:
            logger.exception(f"Error on priceAlert: {e}")

    @discord.app_commands.command(name="my_robosats_alerts",
                                  description="🔍 Show your robosats active alerts 🔍")
    async def my_alerts(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://127.0.0.1:5000/robosats_alerts/{interaction.user.id}/") as r:
                data = await r.json()
                if len(data['ALERTS']) > 0:
                    embed_response = discord.Embed(title="Active alerts")
                    for alert in data['ALERTS']:
                        embed_response.add_field(name=f"ID: {alert['ALERT_ID']}",
                                                 value=f"· Fiat: {alert['FIAT_CURRENCY']}\n"
                                                       f"· Amount: {alert['AMOUNT']}\n"
                                                       f"· Methods: {alert['METHOD']}\n"
                                                       f"· Direction: {alert['DIRECTION']}",
                                                 inline=False)
                    await interaction.response.send_message(embed=embed_response)
                else:
                    await interaction.response.send_message("```You don't have active alerts```")

    @discord.app_commands.command(name="remove_robosats_alert",
                                  description="🔕 Remove your robosats alert 🔕")
    @discord.app_commands.describe(alert_id="Your alert id")
    async def remove_alert(self, interaction: discord.Interaction, alert_id: str):
        removed = False
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://127.0.0.1:5000/robosats_alerts/{interaction.user.id}/") as r:
                data = await r.json()
        for alert in data['ALERTS']:
            if int(alert['ALERT_ID']) == int(alert_id):
                removed = True
                await delete_price_alert_by_id(alert_id,
                                               f"http://127.0.0.1:5000/robosats_alerts/{interaction.user.id}/")
                await interaction.response.send_message("```Your alert was removed```")
        if not removed:
            await interaction.response.send_message(
                content=f"```you have no alert with that id.\nType: /my_alerts to see your alerts id```")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        RoboSatsAlerts(bot)
    )
