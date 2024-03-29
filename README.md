# langsplit
[![Travis status](https://img.shields.io/travis/mindey/langsplit/master.svg?style=flat)](https://travis-ci.org/mindey/langsplit)

NOTE: It merits having a JS browser extension to use this pattern in front-end of web applications, as asking everyone to support it natively.

## Inline translations

```
.:lt:Labas, Pasauli.:ja:ハロー・ワールド!
```

## Multiline translations

```
.:cn
你好，世界
.:en
Hello, World
```

## Usage

```python
from langsplit import splitter

result = splitter.split('''.:cn
你好，世界
.:en
Hello, World''')

original = splitter.convert(result)
```

## Capital letters used for machine translations, e.g.:

```python
# pip install requests

from langsplit.extras import append_machine_translations
append_machine_translations('''.:cn
你好，世界
.:en
Hello, World''', langs=['ru', 'cn', 'lt'], intext=True, use_requests=True)
```

```
.:cn
你好，世界
.:en
Hello, World
.:RU
Привет мир
.:LT
Sveikas pasaulis
```

## If you want, you can post-process transaltions, e.g.:

```python
from langsplit import extras

def post_process(value, lang):
    return value + '123'

extras.post_translate = post_process

extras.append_machine_translations('''.:cn
你好，世界
.:en
Hello, World''', langs=['ru', 'cn', 'lt'], intext=True, use_requests=True)
```
