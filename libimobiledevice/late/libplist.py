from enum import Enum
from ctypes import *
from datetime import datetime
from time import gmtime


LIBPLIST = cdll.LoadLibrary('libplist-2.0.dylib')


FMT_XML = 1
FMT_BINARY = 2

MAC_EPOCH = 978307200


class PlistType(Enum):
    PLIST_BOOLEAN = 0
    PLIST_UINT = 1
    PLIST_REAL = 2
    PLIST_STRING = 3
    PLIST_ARRAY = 4
    PLIST_DICT = 5
    PLIST_DATE = 6
    PLIST_DATA = 7
    PLIST_KEY = 8
    PLIST_UID = 9
    PLIST_NONE = 10


class Node:
    _c_node: c_void_p

    def __init__(self):
        self._c_managed = True

    def __dealloc__(self):
        if self._c_node is not None and self._c_managed:
            LIBPLIST.plist_free(self._c_node)

    def __deepcopy__(self, memo={}) -> 'Node':
        return LIBPLIST.plist_t_to_node(LIBPLIST.plist_copy(self._c_node))

    def copy(self) -> 'Node':
        c_node = LIBPLIST.plist_copy(self._c_node)
        return LIBPLIST.plist_t_to_node(c_node)

    def to_xml(self) -> str:
        out : c_char_p = None
        length = c_uint32(0)
        LIBPLIST.plist_to_xml(self._c_node, out, pointer(length))

        return bytes.decode(bytes(out), 'utf-8')

    def to_bin(self) -> bytes:
        out = c_char_p()
        length = c_uint32(0)
        LIBPLIST.plist_to_bin(self._c_node, out, pointer(length))

        return bytes(out[:length])

    def get_parent(self):
        c_parent = None
        node: Node

        c_parent = LIBPLIST.plist_get_parent(self._c_node)
        if c_parent is None:
            return None

        return LIBPLIST.plist_t_to_node(c_parent)

    def __str__(self):
        return str(self.get_value())


class Bool(Node):
    def __init__(self, value=False):
        if value is False:
            self._c_node = LIBPLIST.plist_new_bool(0)
        else:
            self._c_node = LIBPLIST.plist_new_bool(bool(value))

    def __nonzero__(self):
        return self.get_value()

    def __richcmp__(self, other, op):
        b = self.get_value()
        if op == 0:
            return b < other
        if op == 1:
            return b <= other
        if op == 2:
            return b == other
        if op == 3:
            return b != other
        if op == 4:
            return b > other
        if op == 5:
            return b >= other

    def __repr__(self):
        b = self.get_value()
        return '<Bool: %s>' % b

    def set_value(self, value):
        LIBPLIST.plist_set_bool_val(self._c_node, bool(value))

    def get_value(self) -> bool:
        value = c_uint8()
        LIBPLIST.plist_get_bool_val.argtypes = [c_void_p, POINTER(c_uint8)]
        LIBPLIST.plist_get_bool_val(self._c_node, pointer(value))
        return bool(value)


class Integer(Node):
    def __init__(self, value, signed=False):
        if value is None:
            self._c_node = LIBPLIST.plist_new_uint(0)
        else:
            self._c_node = LIBPLIST.plist_new_uint(int(value))

    def __repr__(self):
        i : c_uint64 = self.get_value()
        return '<Integer: %s>' % i

    def __int__(self):
        return self.get_value()

    def __float__(self):
        return float(self.get_value())

    def __richcmp__(self, other, op):
        i : c_int32 = self.get_value()
        if op == 0:
            return i < other
        if op == 1:
            return i <= other
        if op == 2:
            return i == other
        if op == 3:
            return i != other
        if op == 4:
            return i > other
        if op == 5:
            return i >= other

    def set_value(self, value):
        LIBPLIST.plist_set_uint_val(self._c_node, int(value))

    def get_value(self) -> int:
        result = c_uint64()
        LIBPLIST.plist_get_uint_val.argtypes = [c_void_p, POINTER(c_uint64)]
        LIBPLIST.plist_get_uint_val(self._c_node, pointer(result))
        return result.value


class Real(Node):
    def __init__(self, value):
        if value is None:
            self._c_node = LIBPLIST.plist_new_real(0.0)
        else:
            self._c_node = LIBPLIST.plist_new_real(float(value))

    def __repr__(self):
        r = self.get_value()
        return '<Real: %s>' % r

    def __float__(self):
        return self.get_value()

    def __richcmp__(self, other, op):
        f = self.get_value()
        if op == 0:
            return f < other
        if op == 1:
            return f <= other
        if op == 2:
            return f == other
        if op == 3:
            return f != other
        if op == 4:
            return f > other
        if op == 5:
            return f >= other

    def set_value(self, value):
        LIBPLIST.plist_set_real_val(self._c_node, float(value))

    def get_value(self) -> float:
        value = c_float(0.0)
        LIBPLIST.plist_get_real_val(self._c_node, pointer(value))
        return value



class Uid(Node):
    def __init__(self, value=None):
        if value is None:
            self._c_node = LIBPLIST.plist_new_uid(0)
        else:
            self._c_node = LIBPLIST.plist_new_uid(int(value))

    def __repr__(self):
        i : c_uint64 = self.get_value()
        return '<Uid: %s>' % i

    def __int__(self):
        return self.get_value()

    def __float__(self):
        return float(self.get_value())

    def __richcmp__(self, other, op):
        i : c_int32 = self.get_value()
        if op == 0:
            return i < other
        if op == 1:
            return i <= other
        if op == 2:
            return i == other
        if op == 3:
            return i != other
        if op == 4:
            return i > other
        if op == 5:
            return i >= other

    def set_value(self, value):
        LIBPLIST.plist_set_uid_val(self._c_node, int(value))

    def get_value(self) -> c_uint64:
        value: c_uint64
        LIBPLIST.plist_get_uid_val(self._c_node, pointer(value))
        return value




class Key(Node):
    def __init__(self, value=None):
        c_utf8_data = None
        utf8_data : bytes
        if value is None:
            raise ValueError("Requires a value")
        else:
            if isinstance(value, str):
                utf8_data = value.encode('utf-8')
            else:
                raise ValueError("Requires unicode input, got %s" % type(value))
            c_utf8_data = utf8_data
            self._c_node = LIBPLIST.plist_new_string("")
            LIBPLIST.plist_set_key_val(self._c_node, c_utf8_data)

    def __repr__(self):
        s = self.get_value()
        return '<Key: %s>' % s.encode('utf-8')

    def __richcmp__(self, other, op):
        s = self.get_value()
        if op == 0:
            return s < other
        if op == 1:
            return s <= other
        if op == 2:
            return s == other
        if op == 3:
            return s != other
        if op == 4:
            return s > other
        if op == 5:
            return s >= other

    def set_value(self, value):
        c_utf8_data = None
        utf8_data : bytes
        if value is None:
            LIBPLIST.plist_set_key_val(self._c_node, c_utf8_data)
        else:
            if isinstance(value, str):
                utf8_data = value.encode('utf-8')
            else:
                raise ValueError("Requires unicode input, got %s" % type(value))
            c_utf8_data = utf8_data
            LIBPLIST.plist_set_key_val(self._c_node, c_utf8_data)

    def get_value(self) -> str:
        c_value = c_char_p()
        LIBPLIST.plist_get_key_val(self._c_node, pointer(c_value))
        return bytes.decode(c_value, 'utf-8')



class String(Node):
    def __init__(self, value=None):
        c_utf8_data = c_char_p()
        if value is None:
            self._c_node = LIBPLIST.plist_new_string("")
        else:
            if isinstance(value, str):
                utf8_data = value.encode('utf-8')
            else:
                raise ValueError("Requires unicode input, got %s" % type(value))
            c_utf8_data = utf8_data
            self._c_node = LIBPLIST.plist_new_string(c_utf8_data)

    def __repr__(self):
        s = self.get_value()
        return '<String: %s>' % s.encode('utf-8')

    def __richcmp__(self, other, op):
        s : str = self.get_value()
        if op == 0:
            return s < other
        if op == 1:
            return s <= other
        if op == 2:
            return s == other
        if op == 3:
            return s != other
        if op == 4:
            return s > other
        if op == 5:
            return s >= other

    def set_value(self, value):
        c_utf8_data = None
        utf8_data: bytes
        if value is None:
            LIBPLIST.plist_set_string_val(self._c_node, c_utf8_data)
        else:
            if isinstance(value, str):
                utf8_data = value.encode('utf-8')
            else:
                raise ValueError("Requires unicode input, got %s" % type(value))
            c_utf8_data = utf8_data
            LIBPLIST.plist_set_string_val(self._c_node, c_utf8_data)

    def get_value(self) -> str:
        c_value = c_char_p()
        LIBPLIST.plist_get_string_val.argtypes = [c_void_p, POINTER(c_char_p)]
        LIBPLIST.plist_get_string_val(self._c_node, pointer(c_value))
        return c_value.value


class Date(Node):
    def __init__(self, value = None):
        self._c_node = LIBPLIST.create_date_plist(value)

    def __repr__(self):
        d = self.get_value()
        return '<Date: %s>' % d.ctime()

    def __richcmp__(self, other, op):
        d = self.get_value()
        if op == 0:
            return d < other
        if op == 1:
            return d <= other
        if op == 2:
            return d == other
        if op == 3:
            return d != other
        if op == 4:
            return d > other
        if op == 5:
            return d >= other

    @staticmethod
    def ints_to_datetime(sec: int, usec: int) -> datetime:
        parsed_time = gmtime(sec)
        return datetime(parsed_time.tm_year + 1990, parsed_time.tm_mon, parsed_time.tm_mday, parsed_time.tm_hour,
                        parsed_time.tm_min, parsed_time.tm_sec, usec)

    def get_value(self) -> object:
        secs = c_int32(0)
        usecs = c_int32(0)
        LIBPLIST.plist_get_date_val(self._c_node, pointer(secs), pointer(usecs))
        secs.value += MAC_EPOCH
        return Date.ints_to_datetime(secs.value, usecs.value)

    def set_value(self, value: object):
        secs = c_int32(0)
        usecs = c_int32(0)
        if not LIBPLIST.check_datetime(value):
            raise ValueError("Expected a datetime")
        LIBPLIST.datetime_to_ints(value, pointer(secs), pointer(usecs))
        LIBPLIST.plist_set_date_val(self._c_node, secs, usecs)


class Data(Node):
    def __init__(self, value=None):
        if value is None:
            self._c_node = LIBPLIST.plist_new_data(None, 0)
        else:
            self._c_node = LIBPLIST.plist_new_data(value, len(value))

    def __repr__(self):
        d = self.get_value()
        return '<Data: %s>' % d

    def __richcmp__(self, other, op):
        d : bytes = self.get_value()
        if op == 0:
            return d < other
        if op == 1:
            return d <= other
        if op == 2:
            return d == other
        if op == 3:
            return d != other
        if op == 4:
            return d > other
        if op == 5:
            return d >= other

    def get_value(self) -> bytes:
        val = c_char_p()
        length = c_uint64(0)
        LIBPLIST.plist_get_data_val.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_uint64)]
        LIBPLIST.plist_get_data_val(self._c_node, pointer(val), pointer(length))

        return bytes(val.value)


    def set_value(self, value):
        py_val = value
        LIBPLIST.plist_set_data_val(self._c_node, py_val, len(value))




class Dict(Node):
    def __init__(self, value=None):
        self._c_node = LIBPLIST.create_dict_plist(value)

    def _init(self):
        it = c_void_p()
        key = c_char_p()
        subnode = c_void_p()

        self._map = {}

        LIBPLIST.plist_dict_new_iter.argtypes = [c_void_p, POINTER(c_void_p)]
        LIBPLIST.plist_dict_new_iter(self._c_node, pointer(it))
        LIBPLIST.plist_dict_next_item.argtypes = [c_void_p, c_void_p, POINTER(c_char_p), POINTER(c_void_p)]
        LIBPLIST.plist_dict_next_item(self._c_node, it, pointer(key), pointer(subnode))

        while subnode is not None:
            py_key = key.value

            if py_key is None:
                break

            py_key = py_key.decode('utf-8')

            self._map[py_key] = plist_t_to_node(subnode, False)
            subnode = c_void_p()
            key = c_char_p()
            LIBPLIST.plist_dict_next_item.argtypes = [c_void_p, c_void_p, POINTER(c_char_p), POINTER(c_void_p)]
            LIBPLIST.plist_dict_next_item(self._c_node, it, pointer(key), pointer(subnode))

    def __dealloc__(self):
        self._map = None

    def __richcmp__(self, other, op):
        d : dict = self.get_value()
        if op == 0:
            return d < other
        if op == 1:
            return d <= other
        if op == 2:
            return d == other
        if op == 3:
            return d != other
        if op == 4:
            return d > other
        if op == 5:
            return d >= other

    def __len__(self):
        return len(self._map)

    def __repr__(self):
        return '<Dict: %s>' % self._map

    def get_value(self) -> dict:
        return dict([(key, value.get_value()) for key, value in self.items()])

    def set_value(self, value : dict):
        LIBPLIST.plist_free(self._c_node)
        self._map = {}
        self._c_node = None
        self._c_node = LIBPLIST.create_dict_plist(value)
        self._init()

    def __iter__(self):
        return self._map.__iter__()

    def has_key(self, key) -> Bool:
        return self._map.has_key(key)

    def get(self, key, default=None):
        return self._map.get(key, default)

    def keys(self) -> list:
        return self._map.keys()

    def iterkeys(self):
        return self._map.iterkeys()

    def items(self) -> list:
        return self._map.items()

    def iteritems(self):
        return self._map.iteritems()

    def values(self) -> list:
        return self._map.values()

    def itervalues(self):
        return self._map.itervalues()

    def __getitem__(self, key):
        return self._map[key]

    def __setitem__(self, key, value):
        n: Node
        if isinstance(value, Node):
            n = value.copy()
        else:
            n = LIBPLIST.plist_t_to_node(native_to_plist_t(value), False)

        LIBPLIST.plist_dict_set_item(self._c_node, key, n._c_node)
        self._map[key] = n

    def __delitem__(self, key):
        self._map.__delitem__(key)
        LIBPLIST.plist_dict_remove_item(self._c_node, key)


class Array(Node):
    _array: []

    def __init__(self, value: 'Array'):
        self._c_node = LIBPLIST.create_array_plist(value)

    def _init(self):
        self._array = []
        LIBPLIST.plist_array_get_size.argtypes = [c_void_p]
        LIBPLIST.plist_array_get_size.restype = c_uint32
        size: c_uint32 = LIBPLIST.plist_array_get_size(self._c_node)
        subnode = None

        for i in range(size):
            LIBPLIST.plist_array_get_item.argtypes = [c_void_p, c_uint32]
            LIBPLIST.plist_array_get_item.restype = c_void_p
            subnode = LIBPLIST.plist_array_get_item(self._c_node, i)
            self._array.append(plist_t_to_node(subnode, False))

    def __richcmp__(self, other, op):
        l : list = self.get_value()
        if op == 0:
            return l < other
        if op == 1:
            return l <= other
        if op == 2:
            return l == other
        if op == 3:
            return l != other
        if op == 4:
            return l > other
        if op == 5:
            return l >= other

    def __len__(self):
        return len(self._array)

    def __repr__(self):
        return '<Array: %s>' % self._array

    def get_value(self) -> list:
        return [i.get_value() for i in self]

    def set_value(self, value):
        self._array = []
        LIBPLIST.plist_free(self._c_node)
        self._c_node = None
        self._c_node = LIBPLIST.create_array_plist(value)
        self._init()

    def __iter__(self):
        return self._array.__iter__()

    def __getitem__(self, index):
        return self._array[index]

    def __setitem__(self, index, value):
        n : Node
        if isinstance(value, Node):
            n = value.copy()
        else:
            n = LIBPLIST.plist_t_to_node(native_to_plist_t(value), False)

        if index < 0:
            index = len(self) + index

        LIBPLIST.plist_array_set_item(self._c_node, n._c_node, index)
        self._array[index] = n

    def __delitem__(self, index):
        if index < 0:
            index = len(self) + index
        del self._array[index]
        LIBPLIST.plist_array_remove_item(self._c_node, index)

    def append(self, item):
        n: Node

        if isinstance(item, Node):
            n = item.copy()
        else:
            n = LIBPLIST.plist_t_to_node(native_to_plist_t(item), False)

        LIBPLIST.plist_array_append_item(self._c_node, n._c_node)
        self._array.append(n)


def from_xml(xml: bytes):
    c_node = c_void_p()

    if isinstance(xml, str):
        xml = bytes(xml, 'utf-8')

    if xml[-1] != b'\0':
        xml = bytearray(xml)
        xml.append(0)
        xml = bytes(xml)

    c_data = c_char_p(xml)
    length = len(xml)

    LIBPLIST.plist_from_xml.argtypes = [c_char_p, c_uint32, POINTER(c_void_p)]
    LIBPLIST.plist_from_xml(c_data, length, pointer(c_node))
    return plist_t_to_node(c_node)


def from_bin(binary: bytes):
    c_node = c_void_p()
    LIBPLIST.plist_from_bin(binary, len(binary), pointer(c_node))
    return plist_t_to_node(c_node)


def native_to_plist_t(native):
    c_node = None
    child_c_node = None
    secs = 0
    usecs = 0
    node = None
    if isinstance(native, Node):
        node = native
        return LIBPLIST.plist_copy(node._c_node)
    if isinstance(native, str):
        return LIBPLIST.plist_new_string(native)
    if isinstance(native, bool):
        return LIBPLIST.plist_new_bool(native)
    if isinstance(native, int) or isinstance(native, c_long):
        return LIBPLIST.plist_new_uint(native)
    if isinstance(native, float):
        return LIBPLIST.plist_new_real(native)
    if isinstance(native, dict):
        return LIBPLIST.create_dict_plist(native)
    if isinstance(native, list) or isinstance(native, tuple):
        return LIBPLIST.create_array_plist(native)
    if LIBPLIST.check_datetime(native):
        return LIBPLIST.create_date_plist(native)


def load(fp, fmt=None, use_builtin_types=True, dict_type=dict) -> object:
    is_binary = fp.read(6) == 'bplist'
    fp.seek(0)

    cb = None

    if not fmt:
        if is_binary:
            if 'b' not in fp.mode:
                raise IOError('File handle must be opened in binary (b) mode to read binary property lists')
            cb = from_bin
        else:
            cb = from_xml
    else:
        if fmt not in (FMT_XML, FMT_BINARY):
            raise ValueError('Format must be constant FMT_XML or FMT_BINARY')
        if fmt == FMT_BINARY:
            cb = from_bin
        elif fmt == FMT_XML:
            cb = from_xml

    if is_binary and fmt == FMT_XML:
        raise ValueError('Cannot parse binary property list as XML')
    elif not is_binary and fmt == FMT_BINARY:
        raise ValueError('Cannot parse XML property list as binary')

    return cb(fp.read())


def loads(data, fmt=None, use_builtin_types=True, dict_type=dict) -> object:
    is_binary = data[0:6] == 'bplist'

    cb = None

    if fmt is not None:
        if fmt not in (FMT_XML, FMT_BINARY):
            raise ValueError('Format must be constant FMT_XML or FMT_BINARY')
        if fmt == FMT_BINARY:
            cb = from_bin
        else:
            cb = from_xml
    else:
        if is_binary:
            cb = from_bin
        else:
            cb = from_xml

    if is_binary and fmt == FMT_XML:
        raise ValueError('Cannot parse binary property list as XML')
    elif not is_binary and fmt == FMT_BINARY:
        raise ValueError('Cannot parse XML property list as binary')

    return cb(data)


def dump(value, fp, fmt=FMT_XML, sort_keys=True, skipkeys=False) -> object:
    fp.write(dumps(value, fmt=fmt))


def dumps(value, fmt=FMT_XML, sort_keys=True, skipkeys=False) -> object:
    if fmt not in (FMT_XML, FMT_BINARY):
        raise ValueError('Format must be constant FMT_XML or FMT_BINARY')

    if LIBPLIST.check_datetime(value):
        node = Date(value)
    elif isinstance(value, str):
        node = String(value)
    elif isinstance(value, bytes):
        node = Data(value)
    elif isinstance(value, str):
        # See if this is binary
        try:
            node = String(value)
        except ValueError:
            node = Data(value)
    elif isinstance(value, bool):
        node = Bool(value)
    elif isinstance(value, int):
        node = Integer(value)
    elif isinstance(value, float):
        node = Real(value)
    elif isinstance(value, dict):
        node = Dict(value)
    elif type(value) in (list, set, tuple):
        node = Array(value)

    if fmt == FMT_XML:
        return node.to_xml()

    return node.to_bin()


def create_array_plist(value=None):
    node = None
    c_node = None
    node = LIBPLIST.plist_new_array()
    if value is not None and (isinstance(value, list) or isinstance(value, tuple)):
        for item in value:
            c_node = LIBPLIST.native_to_plist_t(item)
            LIBPLIST.plist_array_append_item(node, c_node)
            c_node = None
    return node


def Uid_factory(c_node, managed=True) -> Uid:
    instance = Uid.__new__(Uid)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance

def Real_factory(c_node, managed=True) -> Real:
    instance = Real.__new__(Real)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def Dict_factory(c_node, managed=True) -> dict:
    instance = Dict.__new__(Dict)
    instance._c_managed = managed
    instance._c_node = c_node
    instance._init()
    return instance


def Bool_factory(c_node, managed=True) -> Bool:
    instance = Bool.__new__(Bool)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def Key_factory(c_node, managed=True) -> Key:
    instance : Key = Key.__new__(Key)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def Array_factory(c_node, managed=True) -> Array:
    instance = Array.__new__(Array)
    instance._c_managed = managed
    instance._c_node = c_node
    instance._init()
    return instance


def Date_factory(c_node, managed = True) -> Date:
    instance: Date = Date.__new__(Date)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def Integer_factory(c_node, managed=True) -> Integer:
    instance = Integer.__new__(Integer)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def String_factory(c_node, managed = True) -> String:
    instance = String.__new__(String)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def Data_factory(c_node, managed=True) -> Data:
    instance = Data.__new__(Data)
    instance._c_managed = managed
    instance._c_node = c_node
    return instance


def create_dict_plist(value=None):
    node = None
    c_node = None
    node = LIBPLIST.plist_new_dict()
    if value is not None and isinstance(value, dict):
        for key, item in value.items():
            c_node = LIBPLIST.native_to_plist_t(item)
            LIBPLIST.plist_dict_set_item(node, key, c_node)
            c_node = None
    return node


def create_date_plist(value=None):
    node = None
    secs: c_int32
    usecs: c_int32
    if value is None:
        node = LIBPLIST.plist_new_date(0, 0)
    elif LIBPLIST.check_datetime(value):
        LIBPLIST.datetime_to_ints(value, pointer(secs), pointer(usecs))
        secs -= MAC_EPOCH
        node = LIBPLIST.plist_new_date(secs, usecs)
    return node


def plist_t_to_node(c_plist, managed=True):
    LIBPLIST.plist_get_node_type.argtypes = [c_void_p]
    LIBPLIST.plist_get_node_type.restype = c_int32
    t = PlistType(LIBPLIST.plist_get_node_type(c_plist))
    if t == PlistType.PLIST_BOOLEAN:
        return Bool_factory(c_plist, managed)
    if t == PlistType.PLIST_UINT:
        return Integer_factory(c_plist, managed)
    if t == PlistType.PLIST_KEY:
        return Key_factory(c_plist, managed)
    if t == PlistType.PLIST_REAL:
        return Real_factory(c_plist, managed)
    if t == PlistType.PLIST_STRING:
        return String_factory(c_plist, managed)
    if t == PlistType.PLIST_ARRAY:
        return Array_factory(c_plist, managed)
    if t == PlistType.PLIST_DICT:
        return Dict_factory(c_plist, managed)
    if t == PlistType.PLIST_DATE:
        return Date_factory(c_plist, managed)
    if t == PlistType.PLIST_DATA:
        return Data_factory(c_plist, managed)
    if t == PlistType.PLIST_UID:
        return Uid_factory(c_plist, managed)
    if t == PlistType.PLIST_NONE:
        return None


def plist_free(value: object):
    LIBPLIST.plist_free(value)
