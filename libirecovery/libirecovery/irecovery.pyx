#cython: language_level=3

from ctypes import POINTER
from typing import *

import cython, struct

from libc.stdint cimport *

cdef extern from "libirecovery/libirecovery.h":
    ctypedef enum irecv_error_t:
        IRECV_E_SUCCESS = 0
        IRECV_E_NO_DEVICE = -1
        IRECV_E_OUT_OF_MEMORY = -2
        IRECV_E_UNABLE_TO_CONNECT = -3
        IRECV_E_INVALID_INPUT = -4
        IRECV_E_FILE_NOT_FOUND = -5
        IRECV_E_USB_UPLOAD = -6
        IRECV_E_USB_STATUS = -7
        IRECV_E_USB_INTERFACE = -8
        IRECV_E_USB_CONFIGURATION = -9
        IRECV_E_PIPE = -10
        IRECV_E_TIMEOUT = -11
        IRECV_E_UNSUPPORTED = -254
        IRECV_E_UNKNOWN_ERROR = -255

    ctypedef enum irecv_event_type:
        IRECV_RECEIVED = 1
        IRECV_PRECOMMAND = 2
        IRECV_POSTCOMMAND = 3
        IRECV_CONNECTED = 4
        IRECV_DISCONNECTED = 5
        IRECV_PROGRESS = 6

    cdef enum irecv_mode:
        IRECV_K_RECOVERY_MODE_1 = 0x1280
        IRECV_K_RECOVERY_MODE_2 = 0x1281
        IRECV_K_RECOVERY_MODE_3 = 0x1282
        IRECV_K_RECOVERY_MODE_4 = 0x1283
        IRECV_K_WTF_MODE = 0x1222
        IRECV_K_DFU_MODE = 0x1227

    ctypedef enum irecv_device_event_type:
        IRECV_DEVICE_ADD = 1
        IRECV_DEVICE_REMOVE = 2

    cdef struct irecv_device_info:
        unsigned int cpid
        unsigned int cprv
        unsigned int cpfm
        unsigned int scep
        unsigned int bdid
        uint64_t ecid
        unsigned int ibfl
        char * srnm
        char * imei
        char * srtg
        char * serial_string
        unsigned char * ap_nonce
        unsigned int ap_nonce_size
        unsigned char * sep_nonce
        unsigned int sep_nonce_size

    cdef struct irecv_device:
        const char * product_type
        const char * hardware_model
        unsigned int board_id
        unsigned int chip_id
        const char * display_name

    ctypedef struct irecv_event_t:
        int size
        const char * data
        double progress
        irecv_event_type type

    ctypedef struct irecv_device_event_t:
        irecv_device_event_type type
        irecv_mode mode
        irecv_device_info *device_info

    ctypedef irecv_device * irecv_device_t;

    ctypedef struct irecv_client_private:
        pass

    ctypedef irecv_client_private * irecv_client_t

    ctypedef void(*irecv_device_event_cb_t)(const irecv_device_event_t * event, void *user_data)

    ctypedef int(*irecv_event_cb_t)(irecv_client_t client, const irecv_event_t * event)

    ctypedef irecv_device_event_context * irecv_device_event_context_t

    ctypedef struct irecv_device_event_context:
        irecv_device_event_cb_t callback;
        void *user_data;

    void irecv_set_debug_level(int level)
    const char * irecv_strerror(irecv_error_t error)
    void irecv_init()
    void irecv_exit()

    irecv_error_t irecv_open_with_ecid(irecv_client_t * client, uint64_t ecid)
    irecv_error_t irecv_open_with_ecid_and_attempts(irecv_client_t * pclient, uint64_t ecid, int attempts)
    irecv_error_t irecv_reset(irecv_client_t client)
    irecv_error_t irecv_close(irecv_client_t client)
    irecv_client_t irecv_reconnect(irecv_client_t client, int initial_pause)

    irecv_error_t irecv_receive(irecv_client_t client)
    irecv_error_t irecv_execute_script(irecv_client_t client, const char * script)
    irecv_error_t irecv_reset_counters(irecv_client_t client)
    irecv_error_t irecv_finish_transfer(irecv_client_t client)
    irecv_error_t irecv_trigger_limera1n_exploit(irecv_client_t client)

    irecv_error_t irecv_usb_set_configuration(irecv_client_t client, int configuration)
    irecv_error_t irecv_usb_set_interface(irecv_client_t client, int usb_interface, int usb_alt_interface)
    int irecv_usb_control_transfer(irecv_client_t client, uint8_t bm_request_type, uint8_t b_request, uint16_t w_value,
                                   uint16_t w_index, unsigned char *data, uint16_t w_length, unsigned int timeout)
    int irecv_usb_bulk_transfer(irecv_client_t client, unsigned char endpoint, unsigned char *data, int length,
                                int *transferred, unsigned int timeout)

    irecv_error_t irecv_device_event_subscribe(irecv_device_event_context_t *context, irecv_device_event_cb_t callback,
                                               void *user_data)
    irecv_error_t irecv_device_event_unsubscribe(irecv_device_event_context_t context)

    irecv_error_t irecv_event_subscribe(irecv_client_t client, irecv_event_type type, irecv_event_cb_t callback,
                                        void *user_data)
    irecv_error_t irecv_event_unsubscribe(irecv_client_t client, irecv_event_type type)

    irecv_error_t irecv_send_file(irecv_client_t client, const char * filename, int dfu_notify_finished)
    irecv_error_t irecv_send_command(irecv_client_t client, const char * command)
    irecv_error_t irecv_send_command_breq(irecv_client_t client, const char * command, uint8_t b_request)
    irecv_error_t irecv_send_buffer(irecv_client_t client, unsigned char * buffer, unsigned long length,
                                    int dfu_notify_finished)
    irecv_error_t irecv_recv_buffer(irecv_client_t client, char * buffer, unsigned long length)

    irecv_error_t irecv_saveenv(irecv_client_t client)
    irecv_error_t irecv_getenv(irecv_client_t client, const char * variable, char** value)
    irecv_error_t irecv_setenv(irecv_client_t client, const char * variable, const char * value)
    irecv_error_t irecv_reboot(irecv_client_t client)
    irecv_error_t irecv_getret(irecv_client_t client, unsigned int * value)

    irecv_error_t irecv_get_mode(irecv_client_t client, int * mode)
    irecv_device_info * irecv_get_device_info(irecv_client_t client)

    irecv_device_t irecv_devices_get_all()
    irecv_error_t irecv_devices_get_device_by_client(irecv_client_t client, irecv_device_t * device)
    irecv_error_t irecv_devices_get_device_by_product_type(const char * product_type, irecv_device_t * device)
    irecv_error_t irecv_devices_get_device_by_hardware_model(const char * hardware_model, irecv_device_t * device)

irecv_init()


class DeviceError(Exception):
    def __init__(self, error_id: irecv_error_t):
        self._error = error_id
        self._message = irecv_strerror(error_id)

    def __str__(self):
        return self._message


cdef class DeviceInfo:
    cdef irecv_device_info _info

    def __init__(self, irecv_device_info info):
        self._info = info

    @property
    def chip_id(self) -> int:
        return self._info.cpid

    @property
    def exclusive_id(self) -> int:
        return self._info.ecid

    @property
    def chip_revision(self) -> int:
        return self._info.cprv

    @property
    def chip_fuse_mode(self) -> int:
        return self._info.cpfm

    @property
    def board_id(self) -> int:
        return self._info.bdid

    @property
    def security_epoch(self) -> int:
        return self._info.scep

    @property
    def iboot_flags(self) -> int:
        return self._info.ibfl

    @property
    def serial_number(self) -> str:
        return bytes(self._info.srnm).decode('utf-u')

    @property
    def imei(self) -> str:
        return bytes(self._info.imei).decode('utf-8')

    

cdef class Device:
    cdef irecv_client_t _client

    def __init__(self, ecid : Union[str, int], attempts : Optional[int] = None):
        self._client = cython.NULL

        cdef irecv_error_t error_result

        if isinstance(ecid, str):
            ecid = struct.unpack(">Q", bytes(bytearray.fromhex(ecid)))

        if attempts:
            error_result = irecv_open_with_ecid_and_attempts(&self._client, ecid, attempts)
        else:
            error_result = irecv_open_with_ecid(&self._client, ecid)

        if error_result != irecv_error_t.IRECV_E_SUCCESS:
            raise DeviceError(error_result)

    def __del__(self):
        if self._client != cython.NULL:
            error_result = irecv_close(self._client)
            self._client = cython.NULL

    def __getitem__(self, item):
        return self.getenv(item)

    def __setitem__(self, key, value):
        self.setenv(key, value)

    @staticmethod
    def _handle_error(irecv_error_t error):
        if error != irecv_error_t.IRECV_E_SUCCESS:
            raise DeviceError(error)

    def close(self):
        Device._handle_error(irecv_close(self._client))

    def reset(self):
        Device._handle_error(irecv_reset(self._client))

    def reconnect(self, initial_pause: int):
        self._client = irecv_reconnect(self._client, initial_pause)

    def saveenv(self):
        Device._handle_error(irecv_saveenv(self._client))

    def getenv(self, name: str) -> str:
        cdef char* result
        Device._handle_error(irecv_getenv(self._client, name, &result))
        return bytes(result).decode('utf-8')

    def reboot(self):
        Device._handle_error(irecv_reboot(self._client))

    def getret(self) -> int:
        cdef unsigned int result
        Device._handle_error(irecv_getret(self._client, &result))
        return result

    def setenv(self, key: str, value: str):
        Device._handle_error(irecv_setenv(self._client, key, value))

    @property
    def info(self):
        return DeviceInfo(irecv_get_device_info(self._client))

    @property
    def opened(self):
        return self._client != cython.NULL

    @property
    def mode(self) -> irecv_mode:
        cdef irecv_mode mode
        Device._handle_error(irecv_get_mode(self._client, &mode))
        return mode
