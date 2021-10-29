from ctypes import *
from typing import *


def parse_c_string_list(list) -> List[str]:
    result = []

    index = 0
    domain = list[index]
    while domain is not None:
        result.append(domain.decode('utf-8'))
        index += 1
        domain = list[index]

    return result
