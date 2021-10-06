from enum import Enum
from ctypes import *


def describe_plist_dict():
    LIBPLIST = cdll.LoadLibrary('libplist-2.0.dylib')

    def it_should_build_a_dict():
        LIBPLIST.plist_new_dict.restype = c_void_p
        plist_dict = LIBPLIST.plist_new_dict()
        LIBPLIST.plist_dict_get_size.argtypes = [c_void_p]
        assert(LIBPLIST.plist_dict_get_size(plist_dict) == 0)

    def it_should_build_a_dict_and_set_a_key():
        LIBPLIST.plist_new_dict.restype = c_void_p
        plist_dict = LIBPLIST.plist_new_dict()
        LIBPLIST.plist_dict_get_size.argtypes = [c_void_p]

        LIBPLIST.plist_new_bool.argtypes = [c_uint8]
        LIBPLIST.plist_new_bool.restype = c_void_p
        plist_true = LIBPLIST.plist_new_bool(1)

        LIBPLIST.plist_dict_set_item.argtypes = [c_void_p, c_char_p, c_void_p]
        LIBPLIST.plist_dict_set_item(plist_dict, b'some_key', plist_true)

        assert(LIBPLIST.plist_dict_get_size(plist_dict) == 1)

    def it_should_build_a_dict_and_seralize():
        LIBPLIST.plist_new_dict.restype = c_void_p
        plist_dict = LIBPLIST.plist_new_dict()
        LIBPLIST.plist_dict_get_size.argtypes = [c_void_p]

        LIBPLIST.plist_new_bool.argtypes = [c_uint8]
        LIBPLIST.plist_new_bool.restype = c_void_p
        plist_true = LIBPLIST.plist_new_bool(1)

        LIBPLIST.plist_dict_set_item.argtypes = [c_void_p, c_char_p, c_void_p]
        LIBPLIST.plist_dict_set_item(plist_dict, b'some_key', plist_true)

        assert(LIBPLIST.plist_dict_get_size(plist_dict) == 1)

        LIBPLIST.plist_to_xml.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_uint32)]
        buffer = c_char_p()
        length = c_uint32(0)
        LIBPLIST.plist_to_xml(plist_dict, pointer(buffer), byref(length))

        print(buffer.value)
        assert(length != 0)