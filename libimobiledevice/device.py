from ctypes import *
from enum import Enum
from libimobiledevice import BaseError
from sys import platform as _platform


def _initialize_bindings():
    if _platform == "linux" or _platform == "linux2":
        module = cdll.LoadLibrary('libimobiledevice-1.0.so')
    elif _platform == "darwin":
        module = cdll.LoadLibrary('libimobiledevice-1.0.dylib')

    module.idevice_new.argtypes = [POINTER(c_void_p), c_char_p]
    module.idevice_free.argtypes = [c_void_p]
    module.idevice_get_udid.argtypes = [c_void_p, POINTER(c_char_p)]
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
        return result.value

    @property
    def handle(self):
        return self._c_handle
