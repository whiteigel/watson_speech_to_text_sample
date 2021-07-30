import os
from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import telebot

S2T_API = os.environ.get('S2T_API')
LT_API = os.environ.get('LT_API')
S2T_URL = os.environ.get('S2T_URL')
LT_URL = os.environ.get('LT_URL')
CHAT_ID = os.environ.get('CHAT_ID')
TG_TOKEN = os.environ.get('TG_TOKEN')
FILENAME = 'PolynomialRegressionandPipelines.mp3'
version_lt = '2018-05-01'
bot = telebot.TeleBot(TG_TOKEN)


def speech_to_text(key, url, file):
    authenticator = IAMAuthenticator(key)
    s2t = SpeechToTextV1(authenticator=authenticator)
    s2t.set_service_url(url)
    count = 0
    result = []
    with open(file, mode="rb") as wav:
        response = s2t.recognize(audio=wav, content_type='audio/mp3')
        res = response.result['results']
    for item in range(len(res)):
        recognized_text = res[count]["alternatives"][0]["transcript"]
        recognized_text = str(recognized_text.capitalize())
        result.append(recognized_text)
        count += 1
    sep = '.\n'
    print(sep.join(result))
    bot.send_message(CHAT_ID, sep.join(result))
    return sep.join(result)


def lang_translator(key, url, text, lang):
    authenticator = IAMAuthenticator(key)
    language_translator = LanguageTranslatorV3(version=version_lt, authenticator=authenticator)
    language_translator.set_service_url(url)
    translation_response = language_translator.translate(text=text, model_id=f'en-{lang}')
    translation = translation_response.get_result()
    res_translation = translation['translations'][0]['translation']
    print(res_translation)
    bot.send_message(CHAT_ID, res_translation)
    return res_translation


if __name__ == '__main__':
    LANG = input(str('Choose a language to translate to: '))
    lang_translator(LT_API, LT_URL, speech_to_text(S2T_API, S2T_URL, FILENAME), LANG)
