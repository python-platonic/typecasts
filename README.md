# typecasts

[![Build Status](https://travis-ci.com/python-platonic/typecasts.svg?branch=master)](https://travis-ci.com/python-platonic/typecasts)
[![Coverage](https://coveralls.io/repos/github/python-platonic/typecasts/badge.svg?branch=master)](https://coveralls.io/github/python-platonic/typecasts?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/typecasts.svg)](https://pypi.org/project/typecasts/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![PyPI - License](https://img.shields.io/pypi/l/typecasts)

Convert from one Python type to another in a centralized way.


## Features

```python
from typecasts import casts

str_to_bytes_coder = casts[str, bytes]

str_to_bytes_coder('boo')
# b'boo'
```

## Installation

```bash
pip install typecasts
```


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [cf0afc42e6f5f3886be1d93b6c56b0f422b3a15a](https://github.com/wemake-services/wemake-python-package/tree/cf0afc42e6f5f3886be1d93b6c56b0f422b3a15a). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/cf0afc42e6f5f3886be1d93b6c56b0f422b3a15a...master) since then.
