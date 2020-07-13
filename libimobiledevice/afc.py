from ctypes import *
from enum import Enum
from libimobiledevice import BaseError, BaseService
from libimobiledevice.service import PropertyListService, LockdownServiceDescriptor
from libimobiledevice.device import Device
from sys import platform as _platform


def initialize_bindings():
    if _platform == "linux" or _platform == "linux2":
        module = cdll.LoadLibrary('libimobiledevice-1.0.so')
    elif _platform == "darwin":
        module = cdll.LoadLibrary('libimobiledevice-1.0.dylib')

    module.afc_client_new.argtypes = [c_void_p, c_void_p, POINTER(c_void_p)]
    module.afc_client_start_service.argtypes = [c_void_p, POINTER(c_void_p), c_char_p]
    module.afc_client_free.argtypes = [c_void_p]
    module.afc_get_device_info.argtypes = [c_void_p, POINTER(POINTER(c_char_p))]
    module.afc_read_directory.argtypes = [c_void_p, c_char_p, POINTER(POINTER(c_char_p))]
    module.afc_get_file_info.argtypes = [c_void_p, c_char_p, POINTER(POINTER(c_char_p))]
    module.afc_file_open.argtypes = [c_void_p, c_char_p, c_uint32, POINTER(c_uint64)]
    module.afc_file_close.argtypes = [c_void_p, c_uint64]
    module.afc_file_lock.argtypes = [c_void_p, c_uint64, c_uint32]
    module.afc_file_read.argtypes = [c_void_p, c_uint64, c_char_p, c_uint32, POINTER(c_uint32)]
    module.afc_file_write.argtypes = [c_void_p, c_uint64, c_char_p, c_uint32, POINTER(c_uint32)]
    module.afc_file_seek.argtypes = [c_void_p, c_uint64, c_uint64, c_int32]
    module.afc_file_tell.argtypes = [c_void_p, c_uint64, POINTER(c_uint64)]
    module.afc_file_truncate.argtypes = [c_void_p, c_uint64, c_uint64]
    module.afc_remove_path.argtypes = [c_void_p, c_char_p]
    module.afc_rename_path.argtypes = [c_void_p, c_char_p, c_char_p]
    module.afc_make_directory.argtypes = [c_void_p, c_char_p]
    module.afc_truncate.argtypes = [c_void_p, c_char_p, c_uint64]
    module.afc_make_link.argtypes = [c_void_p, c_int32, c_char_p, c_char_p]
    module.afc_set_file_time.argtypes = [c_void_p, c_char_p, c_uint64]
    module.afc_remove_path_and_contents.argtypes = [c_void_p, c_char_p]
    module.afc_get_device_info_key.argtypes = [c_void_p, c_char_p, POINTER(c_char_p)]

    return module


LIBIMOBILEDEVICE = initialize_bindings()


class AfcErrorCode(Enum):
    AFC_E_SUCCESS = 0
    AFC_E_UNKNOWN_ERROR = 1
    AFC_E_OP_HEADER_INVALID = 2
    AFC_E_NO_RESOURCES = 3
    AFC_E_READ_ERROR = 4
    AFC_E_WRITE_ERROR = 5
    AFC_E_UNKNOWN_PACKET_TYPE = 6
    AFC_E_INVALID_ARG = 7
    AFC_E_OBJECT_NOT_FOUND = 8
    AFC_E_OBJECT_IS_DIR = 9
    AFC_E_PERM_DENIED = 10
    AFC_E_SERVICE_NOT_CONNECTED = 11
    AFC_E_OP_TIMEOUT = 12
    AFC_E_TOO_MUCH_DATA = 13
    AFC_E_END_OF_DATA = 14
    AFC_E_OP_NOT_SUPPORTED = 15
    AFC_E_OBJECT_EXISTS = 16
    AFC_E_OBJECT_BUSY = 17
    AFC_E_NO_SPACE_LEFT = 18
    AFC_E_OP_WOULD_BLOCK = 19
    AFC_E_IO_ERROR = 20
    AFC_E_OP_INTERRUPTED = 21
    AFC_E_OP_IN_PROGRESS = 22
    AFC_E_INTERNAL_ERROR = 23
    AFC_E_MUX_ERROR = 30
    AFC_E_NO_MEM = 31
    AFC_E_NOT_ENOUGH_DATA = 32
    AFC_E_DIR_NOT_EMPTY = 33


class AfcFileMode(Enum):
    AFC_FOPEN_RDONLY = 0x00000001
    AFC_FOPEN_RW = 0x00000002
    AFC_FOPEN_WRONLY = 0x00000003
    AFC_FOPEN_WR = 0x00000004
    AFC_FOPEN_APPEND = 0x00000005
    AFC_FOPEN_RDAPPEND = 0x00000006


class AfcLinkType(Enum):
    AFC_HARDLINK = 1
    AFC_SYMLINK = 2


class AfcLockOperation(Enum):
    AFC_LOCK_SH = 1 | 4
    AFC_LOCK_EX = 2 | 4
    AFC_LOCK_UN = 8 | 4


LOCK_SH = AfcLockOperation.AFC_LOCK_SH
LOCK_EX = AfcLockOperation.AFC_LOCK_EX
LOCK_UN = AfcLockOperation.AFC_LOCK_UN


def afc_mode_to_c_mode(mode):
    if mode == b'r':
        return AfcFileMode.AFC_FOPEN_RDONLY
    elif mode == b'r+':
        return AfcFileMode.AFC_FOPEN_RW
    elif mode == b'w':
        return AfcFileMode.AFC_FOPEN_WRONLY
    elif mode == b'w+':
        return AfcFileMode.AFC_FOPEN_WR
    elif mode == b'a':
        return AfcFileMode.AFC_FOPEN_APPEND
    elif mode == b'a+':
        return AfcFileMode.AFC_FOPEN_RDAPPEND
    else:
        raise ValueError("mode string must be 'r', 'r+', 'w', 'w+', 'a', or 'a+'")


class AfcError(BaseError):
    def __init__(self, error_code: int):
        self._lookup_table = {
            AfcErrorCode.AFC_E_SUCCESS: "Success",
            AfcErrorCode.AFC_E_UNKNOWN_ERROR: "Unknown error",
            AfcErrorCode.AFC_E_OP_HEADER_INVALID: "OP header invalid",
            AfcErrorCode.AFC_E_NO_RESOURCES: "No resources",
            AfcErrorCode.AFC_E_READ_ERROR: "Read error",
            AfcErrorCode.AFC_E_WRITE_ERROR: "Write error",
            AfcErrorCode.AFC_E_UNKNOWN_PACKET_TYPE: "Unknown packet type",
            AfcErrorCode.AFC_E_INVALID_ARG: "Invalid argument",
            AfcErrorCode.AFC_E_OBJECT_NOT_FOUND: "Object not found",
            AfcErrorCode.AFC_E_OBJECT_IS_DIR: "Object is directory",
            AfcErrorCode.AFC_E_PERM_DENIED: "Permission denied",
            AfcErrorCode.AFC_E_SERVICE_NOT_CONNECTED: "Service not connected",
            AfcErrorCode.AFC_E_OP_TIMEOUT: "OP timeout",
            AfcErrorCode.AFC_E_TOO_MUCH_DATA: "Too much data",
            AfcErrorCode.AFC_E_END_OF_DATA: "End of data",
            AfcErrorCode.AFC_E_OP_NOT_SUPPORTED: "OP not supported",
            AfcErrorCode.AFC_E_OBJECT_EXISTS: "Object exists",
            AfcErrorCode.AFC_E_OBJECT_BUSY: "Object busy",
            AfcErrorCode.AFC_E_NO_SPACE_LEFT: "No space left",
            AfcErrorCode.AFC_E_OP_WOULD_BLOCK: "OP would block",
            AfcErrorCode.AFC_E_IO_ERROR: "IO error",
            AfcErrorCode.AFC_E_OP_INTERRUPTED: "OP interrupted",
            AfcErrorCode.AFC_E_OP_IN_PROGRESS: "OP in progress",
            AfcErrorCode.AFC_E_INTERNAL_ERROR: "Internal error",
            AfcErrorCode.AFC_E_MUX_ERROR: "MUX error",
            AfcErrorCode.AFC_E_NO_MEM: "No memory",
            AfcErrorCode.AFC_E_NOT_ENOUGH_DATA: "Not enough data",
            AfcErrorCode.AFC_E_DIR_NOT_EMPTY: "Directory not empty"
        }
        BaseError.__init__(self, error_code)


class AfcFile(object):
    _client: 'AfcClient'

    def __init__(self):
        raise TypeError("AfcFile cannot be instantiated")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.handle_error(LIBIMOBILEDEVICE.afc_file_close(self._client.client, self._c_handle))

    def lock(self, operation: AfcLockOperation):
        self.handle_error(LIBIMOBILEDEVICE.afc_file_lock(self._client.client, self._c_handle, operation))

    def seek(self, offset: c_int64, whence: c_int32):
        self.handle_error(LIBIMOBILEDEVICE.afc_file_seek(self._client.client, self._c_handle, offset, whence))

    def tell(self) -> c_uint64:
        position = c_uint64(0)
        self.handle_error(LIBIMOBILEDEVICE.afc_file_tell(self._client.client, self._c_handle, pointer(position)))
        return position

    def truncate(self, newsize: c_uint64):
        self.handle_error(LIBIMOBILEDEVICE.afc_file_truncate(self._client.client, self._c_handle, newsize))

    def read(self, size: c_uint32) -> bytes:

        bytes_read = c_uint32(0)
        c_data = create_string_buffer(size)
        result: bytes
        try:
            self.handle_error(
                LIBIMOBILEDEVICE.afc_file_read(self._client.client, self._c_handle, c_data, size, pointer(bytes_read)))
            result = c_data[:bytes_read]
            return result
        except BaseError as e:
            raise e
        finally:
            free(c_data)

    def write(self, data: bytes) -> c_uint32:
        bytes_written = c_uint32()
        c_data: bytes
        try:
            self.handle_error(LIBIMOBILEDEVICE.afc_file_write(self._client.client, self._c_handle, c_data, len(data),
                                                              pointer(bytes_written)))
        except BaseError as e:
            raise

        return bytes_written

    def _error(self, ret: c_uint16) -> AfcError:
        return AfcError(ret)


class AfcClient(BaseService):
    __service_name__ = "com.apple.afc"
    _c_client: c_void_p

    def __init__(self, device: Device = None, descriptor: LockdownServiceDescriptor = None):
        self._c_client = c_void_p()
        if device is None and descriptor is None:
            raise ArgumentError("device or descriptor must be provided")

        if descriptor is None:
            self.handle_error(LIBIMOBILEDEVICE.afc_client_start_service(device.handle, pointer(self._c_client), b'libimobiledevice'))
        else:
            self.handle_error(LIBIMOBILEDEVICE.afc_client_new(device.handle, descriptor, pointer(self._c_client)))

    def __dealloc__(self):
        err = c_int16()
        if self._c_client is not None:
            err = LIBIMOBILEDEVICE.afc_client_free(self._c_client)
            self.handle_error(err)

    def _error(self, ret: c_uint16) -> AfcError:
        return AfcError(ret)

    @property
    def client(self) -> c_void_p:
        return self._c_client

    def get_device_info(self) -> list:
        err = c_int16()
        infos: c_void_p()
        info: bytes
        i = 0
        result = []
        err = LIBIMOBILEDEVICE.afc_get_device_info(self._c_client, pointer(infos))
        try:
            self.handle_error(err)
        except BaseError as e:
            raise
        finally:
            if infos is not None:
                while infos[i]:
                    info = infos[i]
                    result.append(info)
                    free(infos[i])
                    i = i + 1
                free(infos)

        return result

    def read_directory(self, directory: str) -> list:
        err = c_int16(0)
        dir_list = c_void_p()
        f: bytes
        i = 0
        result = []
        err = LIBIMOBILEDEVICE.afc_read_directory(self._c_client, directory, pointer(dir_list))
        try:
            self.handle_error(err)
        except BaseError as e:
            raise
        finally:
            if dir_list is not None:
                while dir_list[i]:
                    f = dir_list[i]
                    result.append(f)
                    free(dir_list[i])
                    i = i + 1
                free(dir_list)

        return result

    def open(self, filename: str, mode: bytes = b'r') -> AfcFile:
        handle = c_void_p()
        c_mode = afc_mode_to_c_mode(mode)

        self.handle_error(LIBIMOBILEDEVICE.afc_file_open(self._c_client, filename, c_mode, pointer(handle)))
        f = AfcFile.__new__(AfcFile)
        f._c_handle = handle
        f._client = self
        f._filename = filename

        return f

    def get_file_info(self, path: str) -> list:
        result = []
        c_result = c_void_p()
        i = 0
        info: bytes
        try:
            self.handle_error(LIBIMOBILEDEVICE.afc_get_file_info(self._c_client, path, pointer(c_result)))
        except BaseError as e:
            raise
        finally:
            if c_result is not None:
                while c_result[i]:
                    info = c_result[i]
                    result.append(info)
                    free(c_result[i])
                    i = i + 1
                free(c_result)

        return result

    def remove_path(self, path: str):
        self.handle_error(LIBIMOBILEDEVICE.afc_remove_path(self._c_client, path))

    def rename_path(self, f: str, t: bytes):
        self.handle_error(LIBIMOBILEDEVICE.afc_rename_path(self._c_client, f, t))

    def make_directory(self, d: str):
        self.handle_error(LIBIMOBILEDEVICE.afc_make_directory(self._c_client, d))

    def truncate(self, path: str, newsize: c_uint64):
        self.handle_error(LIBIMOBILEDEVICE.afc_truncate(self._c_client, path, newsize))

    def link(self, source: str, link_name: str):
        self.handle_error(LIBIMOBILEDEVICE.afc_make_link(self._c_client, AfcLinkType.AFC_HARDLINK, source, link_name))

    def symlink(self, source: str, link_name: str):
        self.handle_error(LIBIMOBILEDEVICE.afc_make_link(self._c_client, AfcLinkType.AFC_SYMLINK, source, link_name))

    def set_file_time(self, path: str, mtime: c_uint64):
        self.handle_error(LIBIMOBILEDEVICE.afc_set_file_time(self._c_client, path, mtime))


class Afc2Client(AfcClient):
    __service_name__ = "com.apple.afc2"
