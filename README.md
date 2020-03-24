# langsplit
[![Travis status](https://img.shields.io/travis/mindey/langsplit/master.svg?style=flat)](https://travis-ci.org/mindey/langsplit)

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
