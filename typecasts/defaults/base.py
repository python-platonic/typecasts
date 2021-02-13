import json
from functools import partial

from typecasts.main import Typecasts

casts = Typecasts()


casts[dict, str] = json.dumps


# Basic, primitive casts
casts.update({
    (int, float): float,
    (int, bytes): bytes,
})

# String to bytes and vice versa
casts.update({
    (bytes, str): partial(bytes.decode, encoding='utf-8'),
    (str, bytes): str.encode,
})

# Misc experiments
casts.update({
    (float, int): int,
})
