"""Python bindings for libimobiledevice"""

__version__ = '0.3'

from ctypes import c_int16
from typing import Optional


class BaseError(Exception):
    _lookup_table: dict
    _c_errcode: int

    def __init__(self, error_code: int):
        self._c_errcode = error_code
        if self._lookup_table is None:
            self._lookup_table = {}

    def __repr__(self):
        class_name = type(self)
        return f"{class_name}: {self._lookup_table[self._c_errcode]}"


class BaseService(object):
    __service_name__: Optional[str] = None

    def _error(self, error_code: c_int16) -> BaseError:
        return BaseError(error_code)

    def handle_error(self, error: c_int16) -> int:
        if error == 0:
            return 0

        err: BaseError = self._error(error)
        raise err

