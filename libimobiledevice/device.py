from ctypes import *
from ctypes.util import find_library
from enum import Enum
from libimobiledevice import BaseError
from libimobiledevice.util import parse_c_string_list
from sys import platform as _platform
from typing import *


def _initialize_bindings():
    module = cdll.LoadLibrary(find_library('imobiledevice-1.0'))

    module.idevice_new.argtypes = [POINTER(c_void_p), c_char_p]
    module.idevice_free.argtypes = [c_void_p]
    module.idevice_get_udid.argtypes = [c_void_p, POINTER(c_char_p)]
    module.idevice_get_device_list.argtypes = [POINTER(POINTER(c_char_p)), POINTER(c_int)]
    module.idevice_device_list_free.argtypes = [POINTER(c_char_p)]

    return module


LIBIMOBILEDEVICE = _initialize_bindings()


class DeviceErrorCode(Enum):
    IDEVICE_E_SUCCESS = 0
    IDEVICE_E_INVALID_ARG = -1
    IDEVICE_E_UNKNOWN_ERROR = -2
    IDEVICE_E_NO_DEVICE = -3
    IDEVICE_E_NOT_ENOUGH_DATA = -4
    IDEVICE_E_SSL_ERROR = -6
    IDEVICE_E_TIMEOUT = -7


class DeviceError(BaseError):
    def __init__(self, error_code: int):
        self._lookup_table = {
            DeviceErrorCode.IDEVICE_E_SUCCESS: "Success",
            DeviceErrorCode.IDEVICE_E_INVALID_ARG: "Invalid Argument",
            DeviceErrorCode.IDEVICE_E_UNKNOWN_ERROR: "Unknown",
            DeviceErrorCode.IDEVICE_E_NO_DEVICE: "No device",
            DeviceErrorCode.IDEVICE_E_NOT_ENOUGH_DATA: "Not enough data",
            DeviceErrorCode.IDEVICE_E_SSL_ERROR: "SSL Error",
            DeviceErrorCode.IDEVICE_E_TIMEOUT: "Timeout"
        }
        BaseError.__init__(self, error_code)


class Device(object):
    _c_handle: c_void_p

    def __init__(self, udid: str):
        self._c_handle = c_void_p()
        device_id = create_string_buffer(bytes(udid, 'utf-8'))
        self._handle_error(LIBIMOBILEDEVICE.idevice_new(pointer(self._c_handle), device_id))

    def __del__(self):
        if self._c_handle:
            self._handle_error(LIBIMOBILEDEVICE.idevice_free(self._c_handle))

    @staticmethod
    def _handle_error(error_code: int):
        error = DeviceErrorCode(error_code)
        if error != DeviceErrorCode.IDEVICE_E_SUCCESS:
            raise DeviceError(error_code)

    @property
    def udid(self) -> bytes:
        result = c_char_p()
        self._handle_error(LIBIMOBILEDEVICE.idevice_get_udid(self._c_handle, pointer(result)))
        return result.value.decode('utf-8')

    @property
    def handle(self):
        return self._c_handle

    @staticmethod
    def devices() -> List[str]:
        list = pointer(c_char_p())
        count = c_int(0)

        result = DeviceErrorCode(LIBIMOBILEDEVICE.idevice_get_device_list(byref(list), byref(count)))
        if result != DeviceErrorCode.IDEVICE_E_SUCCESS:
            raise DeviceError(result)

        devices = parse_c_string_list(list)

        free_result = LIBIMOBILEDEVICE.idevice_device_list_free(list)

        return devices