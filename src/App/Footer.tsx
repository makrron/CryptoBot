import { memo } from "react";
import { GlFooter } from "gitlanding/GlFooter";
import { declareComponentKeys } from "i18n";
export const Footer = memo(() => {
	return <GlFooter
		bottomDivContent={("Made with ❤️ by Makrron")}
		//email="email@email.com"
		iconLinks={[
			{
				"iconUrl": "https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a69f118df70ad7828d4_icon_clyde_blurple_RGB.svg",
				"href": "https://discord.gg/5rQ9Y9e4Ah",
			},
			{
				"iconUrl": "https://github.com/favicon.ico",
				"href": "https://twitter.com/makrron",
			}
		]}
	/>
})

export const { i18n } = declareComponentKeys<
	| "license"
	| "link1label"
	| "link2label"
	| "link3label"
>()({ Footer });
