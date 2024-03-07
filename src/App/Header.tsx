import { memo } from "react";
import { GlHeader } from "gitlanding/GlHeader";
import {declareComponentKeys} from "i18nifty";

export const Header = memo(() => {
	return <><GlHeader
			title={<h1 style={{ color: 'darkgoldenrod' }}>{"CryptoBot 🤖"}</h1>}		links={[
			{
				"label": ("Documentation"),
				"href": "",
				"onClick": () => window.open("https://cryptobot-1.gitbook.io/documentation/", "_blank")
			},
			{
				"label": ("GitHub"),
				"href": "",
				"onClick": () => window.open("https://github.com/makrron/CryptoBot", "_blank")
			},
			{
				"label": ("Add to Discord"),
				"href": "",
				"onClick": () => window.open("https://discord.com/oauth2/authorize?client_id=860134458308821042&permissions=8&scope=bot", "_blank")
			},
			{
				"label": ("Premium"),
				"href": "",
				"onClick": () => window.open("https://mee6.xyz/es/m/cryptobot", "_blank")

			},
		]}
		enableDarkModeSwitch={false}
	/>

	</>;
});

export const { i18n } = declareComponentKeys<
	| "headerTitle"
	| "link1label"
	| "link2label"
	| "link3label"
>()({ Header });
