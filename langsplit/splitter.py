import os
import collections

import langdetect

LANGUAGE_CODES = os.listdir(langdetect.PROFILES_DIRECTORY)
SHORTER_CODES = {'zh-cn': 'cn', 'zh-tw': 'zh'}

def detect_language(text, max_length=2):
    """ Make sure we return max_length[-letter] keys for languages"""
    code = langdetect.detect(text)
    short_code = SHORTER_CODES.get(code) if len(code) > max_length else code
    return short_code[:max_length]

def split(text, sep='.:', ends=['\n', ':'], min_key_length=2, max_key_length=2,
          autodetect=True, pargraph_sep='\n\n', markdown=False, title=False):
    """
    Splits text by `sep`, and combines texts with same keys before `ends`,
    if they are not shorter/longer than `min_key_length` and `max_key_length`.
    Assigns the rest of the parts to key called None. Returns a dict.

    Detects language if not present, treating each paragraph separately.

    Tip: 
         Change 'markdown' to True to get result combined back to markdown.
         Pass title=True to convert to title version, using the ':' as end.
    """

    result = collections.defaultdict(str)
    lang_seq = []

    for token in text.split(sep):
        if not token:
            continue

        name = None
        chunk = token

        if len(token[:max_key_length+1]) == max_key_length+1:

            for symbol in ends:
                pos = token[:max_key_length+1].find(symbol)

                if min_key_length <= pos <= max_key_length:
                    name, chunk = token[:pos], token[pos+1:]

        if not name:
            if autodetect:

                paragraphs = chunk.split(pargraph_sep)
                number_of_paragraphs = len(paragraphs)
                for i, paragraph in enumerate(paragraphs):
                    if not paragraph:
                        continue

                    name = detect_language(paragraph)
                    result[name] += paragraph

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

        text_md = ''

        for lang in lang_seq:
            text_md += '{sep}{lang}{end}{text}'.format(
                sep = sep,
                lang = lang,
                end = ends[0] if not title else ends[1],
                text = result[lang],
            )

        return text_md.strip()

    return result