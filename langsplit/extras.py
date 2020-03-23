try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

def translate(text_to_translate, to_language='auto', from_langage='auto'):
    # Credits: https://github.com/softvar/translatr/blob/master/app/__init__.py#L22
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_language, from_langage, text_to_translate.replace(" ", "+"))

    request = Request(link, headers=agents)
    page = urlopen(request).read().decode('utf-8')

    # import requests
    # request = requests.get(link, headers=agents)
    # page = request.text

    result = page[page.find(before_trans) + len(before_trans):]
    result = result.split("<")[0]
    return result

from langsplit import splitter

def append_machine_translations(text, langs, intext=False):
    ''' e.g.: langs = ['en', 'cn', 'lt'] '''
    split = splitter.split(text)
    olang = next(iter(split))
    first = split[olang]

    if intext:
        if not first.endswith('\n'):
            split[olang] += '\n'

    for lang in langs:
        if lang == olang:
            continue
        glang = lang
        if glang == 'cn':
            glang = 'zh'

        if lang.upper() not in split:
            split[lang.upper()] = translate(first, glang).replace('  ', '\n\n')
            if intext:
                split[lang.upper()] += '\n'

    if intext:
        return splitter.convert(split)

    return split
