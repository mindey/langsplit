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

