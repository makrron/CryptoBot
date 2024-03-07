import { memo } from "react";
import { GlFooter } from "gitlanding/GlFooter";
import { declareComponentKeys, useTranslation } from "i18n";
export const Footer = memo(() => {
	const { t } = useTranslation({ Footer })
	return <GlFooter
		bottomDivContent={t("license")}
		//email="email@email.com"
		//phoneNumber="+33545345676"
		iconLinks={[
			{
				"iconUrl": "https://discord.com/assets/favicon.ico",
				"href": "https://discord.com/application-directory/860134458308821042",
			},
			{
				"iconUrl": "https://github.com/favicon.ico",
				"href": "https://twitter.com/makrron",
			}
		]}
		/*links={[
			{
				"label": t("link1label"),
				...routes.pageExample().link
			},
			{
				"label": t("link2label"),
				"href": "https://example.com",
			},
			{
				"label": t("link3label"),
				"href": "https://example.com",
			},
		]}*/
	/>
})

export const { i18n } = declareComponentKeys<
	| "license"
	| "link1label"
	| "link2label"
	| "link3label"
>()({ Footer });
