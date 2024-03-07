import { memo } from "react";
import { GlHeader } from "gitlanding/GlHeader";
import {declareComponentKeys} from "i18nifty";
//import { declareComponentKeys, useTranslation, useLang } from "i18n";
//import { createLanguageSelect } from "onyxia-ui/LanguageSelect";
//import type { Language } from "i18n";

/*const { LanguageSelect } = createLanguageSelect<Language>({
	"languagesPrettyPrint": {
		"en": "English",
		"fr": "Français"
	}
})*/

export const Header = memo(() => {
	//const { t } = useTranslation({ Header })
	//const { lang, setLang } = useLang();
	return <><GlHeader
			title={<h1 style={{ color: 'darkgoldenrod' }}>{"CryptoBot 🤖"}</h1>}		links={[
			{
				"label": ("Documentation"),
				"href": "https://cryptobot-1.gitbook.io/documentation/",
			},
			{
				"label": ("GitHub"),
				"href": "https://github.com/makrron/CryptoBot",
			},
			{
				"label": ("Add to Discord"),
				"href": "https://discord.com/application-directory/860134458308821042",
			},
		]}
		enableDarkModeSwitch={false}
	/>

	</>;
		/*customItemEnd={{
			"item": <LanguageSelect
				language={lang}
				onLanguageChange={setLang}
				variant="big"
			/>
		}}*/


});

export const { i18n } = declareComponentKeys<
	| "headerTitle"
	| "link1label"
	| "link2label"
	| "link3label"
>()({ Header });
