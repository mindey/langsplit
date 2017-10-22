import pytest
import collections
from langsplit.splitter import split, convert
from langsplit import splitter


def test_none():
    text = None

    expect = None

    result = split(text)

    assert(result == expect)

def test_title():
    text = '.:en:new world.:lt:smart world.:ja:今日は、世界'
    expect = collections.OrderedDict(
        [('en', 'new world'),
         ('lt', 'smart world'),
         ('ja', '今日は、世界')]
    )
    assert(
        split(text) == expect
    )

def test_body():
    text ='''.:en
some text

which is good

.:ru
несколько текста

.:en
so want to try

.:lt
nieko sau, viskas gerai

.:cn
中文也可以的
'''
    expect = collections.OrderedDict(
        [('en', 'some text\n\nwhich is good\n\nso want to try\n\n'),
         ('ru', 'несколько текста\n\n'),
         ('lt', 'nieko sau, viskas gerai\n\n'),
         ('cn', '中文也可以的\n')]
    )

    assert(
        split(text) == expect
    )

def test_partial_autodetect():
    text = 'amazing world.:lt:smart world.:ja:今日は、世界'
    expect = collections.OrderedDict(
        [('en', 'amazing world'),
         ('lt', 'smart world'),
         ('ja', '今日は、世界')]
    )

    result = split(text)

    assert(
        result == expect
    )


def test_autodetect():
    text = '''some text
which is good

несколько текста

so want to try

šienpjovys džemas

中文也可以的
'''
    expect = collections.OrderedDict(
        [('en', 'some text\nwhich is good\n\nso want to try\n\n'),
         ('ru', 'несколько текста\n\n'),
         ('lt', 'šienpjovys džemas\n\n'),
         ('cn', '中文也可以的\n')]
    )

    result = split(text)

    assert(
        result == expect
    )

def test_markdown():

    text = '''中文也可以的

some text
which is good

несколько текста

so want to try

šienpjovys džemas'''

    expect = '''.:cn
中文也可以的

.:en
some text
which is good

so want to try

.:ru
несколько текста

.:lt
šienpjovys džemas'''

    result = split(text, markdown=True)

    assert(
        result == expect
    )

def test_markdown_title():

    text = '''世界，你好.:lt:Sveikas, Pasauli'''

    expect = '.:cn:世界，你好.:lt:Sveikas, Pasauli'

    result = split(text, markdown=True, title=True)

    assert(
        result == expect
    )

def test_convert():

    body = '''.:en
This task was a bit tricky.'''

    expect = '''.:en
This task was a bit tricky.'''

    result = splitter.convert(splitter.split(body))

    assert(
        result == expect
    )


def test_title_convert():

    body = '''.:en:This task was a bit tricky.'''

    expect = '''.:en:This task was a bit tricky.'''

    result = splitter.convert(splitter.split(body), title=True)

    assert(
        result == expect
    )


def test_get_one():

    text = '''.:cn
中文也可以的

.:en
some text
which is good

so want to try

.:ru
несколько текста

.:lt
šienpjovys džemas'''

    expect = '中文也可以的\n\n'

    splitted = split(text)

    result = splitted.get('cn')

    assert(
        result == expect
    )
