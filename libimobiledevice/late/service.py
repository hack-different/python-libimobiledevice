from libimobiledevice import BaseService, BaseError
from libplist import *
from ctypes import *


class LockdownServiceDescriptor:
    pass


class PropertyListService(BaseService):
    def send(self, node: Node):
        self.handle_error(self._send(node._c_node))

    def receive(self) -> object:
        c_node = c_void_p()
        err = self._receive(c_node)
        try:
            self.handle_error(err)

            return plist_t_to_node(c_node)
        except BaseError:
            if c_node is not None:
                plist_free(c_node)
            raise

    def receive_with_timeout(self, timeout_ms):
        c_node = c_void_p()
        err = self._receive_with_timeout(c_node, timeout_ms)
        try:
            self.handle_error(err)

            return plist_t_to_node(c_node)
        except BaseError:
            if c_node is not None:
                plist_free(c_node)
            raise

    def _send(self, node: c_void_p) -> c_int16:
        raise NotImplementedError("send is not implemented")

    def _receive(self, c_node: c_void_p) -> c_int16:
        raise NotImplementedError("receive is not implemented")

    def _receive_with_timeout(self, c_node: c_void_p, timeout_ms: c_int32) -> c_int16:
        raise NotImplementedError("receive_with_timeout is not implemented")