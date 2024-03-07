import { memo } from "react";
import { GlHero } from "gitlanding/GlHero/GlHero";
import { GlArticle } from "gitlanding/GlArticle";
import { GlCards } from "gitlanding/GlCards";
import { GlLogoCard } from "gitlanding/GlCards/GlLogoCard";
import { declareComponentKeys } from "i18n";
import eurIcon from "assets/icons/euros.png";
import yenIcon from "assets/icons/yen.png";
import coin from "assets/icons/coin.png";
import bitcoinIcon from "assets/icons/bitcoin.png";
import ethGasIcon from "assets/icons/ETHgas.png";
import polygasIcon from "assets/icons/polygas.png";
import bscgasIcon from "assets/icons/bscgas.png";
import whaleIcon from "assets/icons/whale.png";
import settingsIcon from "assets/icons/settings.png";
import researchIcon from "assets/icons/research.png";
import newsIcon from "assets/icons/news.png";
import alarmIcon from "assets/icons/alarm.png";
import mascotaImage from "assets/img/mascota.png";


export const Home = memo(() => {
	return (
		<>
			<GlHero
				title={("Best CryptoBot for Discord")}
				subTitle={("Discord bot that allows you to manage your cryptocurrencies. It is open-source and free to use.")}
				illustration={{
					"type": "image",
					"src": mascotaImage,
					"hasShadow": true
				}}
				hasAnimation={true}
				hasLinkToSectionBellow={false}

			/>


			<GlArticle
				title={("Used in more than 1000 servers")}
				body={("CryptoBot is a Discord bot that helps you stay up-to-date on the latest developments in " +
					"the world of cryptocurrencies. With CryptoBot, you can easily view the prices of various " +
					"cryptocurrencies, use Bitcoin tools, check the current price of Bitcoin and more than 5000 " +
					"crypto assets, and more.\n It's source code is freely available for anyone to view, modify, " +
					"and contribute to. This transparency allows for a strong community of developers and users " +
					"to collaborate and improve the bot.\nWhether you're a seasoned crypto investor or just " +
					"starting out, CryptoBot has something for everyone. With a wide range of features and a " +
					"user-friendly interface, it's never been easier to stay on top of the latest crypto trends.\n" +
					"Thank you for choosing CryptoBot. We hope you find it helpful and informative!")}
				buttonLabel={("add to discord")}
				buttonLink={{
					"href": "",
					"onClick": () => window.open("https://discord.com/oauth2/authorize?client_id=860134458308821042&permissions=8&scope=bot", "_blank")
				}}
				/*illustration={{
					"type": "image",
					"src": mascotaImage,
					"hasShadow": true
				}}*/
				hasAnimation={true}
				illustrationPosition="left"
			/>

			<GlCards>
				<GlLogoCard
					title={("💵 Check Prices 💵")}
					paragraph={("view the price of more than 5000 cryptocurrencies in all the fiat currencies.")}
					iconUrls={
						[
							coin,
							eurIcon,
							yenIcon
						]
					}
					overlapIcons={true}
				/>
				<GlLogoCard
					title={("🪙 Bitcoin 🪙")}
					paragraph={("Util commands to get different information about Bitcoin.\nInfo about transactions and," +
						" post raw transactions to the Bitcoin network and more...")}
					iconUrls={[
						bitcoinIcon
					]}
				/>

				<GlLogoCard
					title={("⛏ Check Fees ⛏")}
					paragraph={("Check the fees of the most common blockchains.")}
					iconUrls={[
						ethGasIcon,
						polygasIcon,
						bscgasIcon,
						bitcoinIcon
					]}
					overlapIcons={true}
				/>

				<GlLogoCard
					title={("💎 Premium Functions 💎")}
					paragraph={("Get access to the premium features of the bot.\n Use exclusive functions as News Feed," +
						"Price Alerts, Price Loop, Whales Alerts and more...")}
					iconUrls={[
						alarmIcon,
						newsIcon,
						researchIcon,
						settingsIcon,
						whaleIcon
					]}
					overlapIcons={false}
				/>
			</GlCards>
		</>
	);
});

export const { i18n } = declareComponentKeys<
	| "heroTitle"
	| "heroSubtitle"
	| "articleTitle"
	| "articleBody"
	| "articleButtonLabel"
	| "card1Title"
	| "card2Title"
	| "card3Title"
	| "card1Paragraph"
	| "card2Paragraph"
	| "card3Paragraph"
>()({ Home });