"""Contains unrelated bot functions used in ``cogs/`` """
import random

import discord

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


async def sendAdEmbed(self, interaction: discord.Interaction, embed):
    try:
        ad_embed = discord.Embed(title=get_promo(), url="https://discord.gg/nNRKgYkvj9",
                                 color=0xf90206)
        embed.set_footer(text=get_promo(), icon_url=self.bot.user.default_avatar)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name=f"{get_bot_status()}"))
        return await interaction.response.send_message(embeds=[ad_embed, embed])
    except Exception:
        return await interaction.response.send_message(embed=embed)
