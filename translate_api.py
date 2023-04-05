from pygtrans import Translate
import logging

client = Translate()

# zh-CN
def translate(text, dest='en', src='auto'):
    logging.info(f'trans input src:{src}, dest:{dest}')
    if '' == text:
        return ''
    # res = translator.translate(text, dest=dest, src=src)
    res = client.translate(text, source=src, target=dest)
    return res.translatedText