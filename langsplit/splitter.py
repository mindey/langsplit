import os
import collections
import logging

import langdetect

class Settings:
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    UNKNOWN_LANGUAGE = 'xx'


settings = Settings()

logging.basicConfig(
    format = settings.LOGGING_FORMAT,
    level = logging.INFO
)
logger = logging.getLogger(__name__)

LANGUAGE_CODES = os.listdir(langdetect.PROFILES_DIRECTORY)
SHORTER_CODES = {'zh-cn': 'cn', 'zh-tw': 'zh'}

def detect_language(text, max_length=2):
    """ Make sure we return max_length[-letter] keys for languages"""
    code = langdetect.detect(text)
    short_code = SHORTER_CODES.get(code) if len(code) > max_length else code
    return short_code[:max_length]

def convert(LanguagesDict, sep='.:', ends=['\n', ':'], title=False):
    text_md = ''

    for lang in LanguagesDict.keys():
        text_md += '{sep}{lang}{end}{text}'.format(
            sep = sep,
            lang = lang,
            end = ends[0] if not title else ends[1],
            text = LanguagesDict[lang],
        )
    return text_md.strip()

def split(text, sep='.:', ends=['\n', ':'], min_key_length=2, max_key_length=2,
          autodetect=True, pargraph_sep='\n\n', markdown=False, title=False):
    """
    Splits text by `sep`, and combines texts with same keys before `ends`,
    if they are not shorter/longer than `min_key_length` and `max_key_length`.
    Assigns the rest of the parts to key called settings.UNKNOWN_LANGUAGE.
    Returns a dict.

    Detects language if not present, treating each paragraph separately.

    Tip: 
         Change 'markdown' to True to get result combined back to markdown.
         Pass title=True to convert to title version, using the ':' as end.
    """
    if not text:
        return text

    result = collections.defaultdict(str)
    lang_seq = []

    for token in text.split(sep):
        if not token:
            continue

        name = settings.UNKNOWN_LANGUAGE
        chunk = token

        if len(token[:max_key_length+1]) == max_key_length+1:

            for symbol in ends:
                pos = token[:max_key_length+1].find(symbol)

                if min_key_length <= pos <= max_key_length:
                    name, chunk = token[:pos], token[pos+1:]

                    if chunk[:len(name)+1] in [name+end for end in ends]:
                        chunk = chunk[len(name)+1:]

        if name == settings.UNKNOWN_LANGUAGE:
            if autodetect:

                paragraphs = chunk.split(pargraph_sep)
                number_of_paragraphs = len(paragraphs)
                for i, paragraph in enumerate(paragraphs):
                    if not paragraph:
                        continue

                    try:
                        name = detect_language(paragraph)
                        result[name] += paragraph

                    except Exception as e:
                        result[settings.UNKNOWN_LANGUAGE] += paragraph
                        logger.info('Language not detected: {}'.format(paragraph))

                    if i < number_of_paragraphs - 1:
                        result[name] += pargraph_sep

                    if name not in lang_seq:
                        lang_seq.append(name)

            else:
                result[name] += chunk

                if name not in lang_seq:
                    lang_seq.append(name)
        else:
            result[name] += chunk

            if name not in lang_seq:
                lang_seq.append(name)

    result = collections.OrderedDict(
        [(lang, result[lang]) for lang in lang_seq]
    )


    if markdown:
        return convert(result, sep=sep, ends=ends, title=title)

    return result
