import { memo } from "react";
import { GlFooter } from "gitlanding/GlFooter";
import { declareComponentKeys, useTranslation } from "i18n";
export const Footer = memo(() => {
	const { t } = useTranslation({ Footer })
	return <GlFooter
		bottomDivContent={t("license")}
		email="email@email.com"
		iconLinks={[
			{
				"iconUrl": "https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a69f118df70ad7828d4_icon_clyde_blurple_RGB.svg",
				"href": "https://discord.com/application-directory/860134458308821042",
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
