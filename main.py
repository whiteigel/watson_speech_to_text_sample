import os
from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

S2T_API = os.environ.get('S2T_API')
LT_API = os.environ.get('LT_API')
S2T_URL = os.environ.get('S2T_URL')
LT_URL = os.environ.get('LT_URL')
FILENAME = 'PolynomialRegressionandPipelines.mp3'
version_lt = '2018-05-01'


def speech_to_text(key, url, file):
    authenticator = IAMAuthenticator(key)
    s2t = SpeechToTextV1(authenticator=authenticator)
    s2t.set_service_url(url)
    with open(file, mode="rb") as wav:
        response = s2t.recognize(audio=wav, content_type='audio/mp3')
        res = response.result
    recognized_text = res['results'][0]["alternatives"][0]["transcript"]
    print(recognized_text)
    return recognized_text


def lang_translator(key, url, text, lang):
    authenticator = IAMAuthenticator(key)
    language_translator = LanguageTranslatorV3(version=version_lt, authenticator=authenticator)
    language_translator.set_service_url(url)
    translation_response = language_translator.translate(text=text, model_id=f'en-{lang}')
    translation = translation_response.get_result()
    res_translation = translation['translations'][0]['translation']
    print(res_translation)
    return res_translation


if __name__ == '__main__':
    LANG = input(str('Choose a language to translate to: '))
    lang_translator(LT_API, LT_URL, speech_to_text(S2T_API, S2T_URL, FILENAME), LANG)
