# python-libimobiledevice

Python bindings for https://github.com/libimobiledevice and it's related family of libraries.

## Comes in two flavors:

* Early bindings which are Cython generated libraries that import the headers from `libimobiledevice` and friends
* Late bindings which are pure python (but use `ctypes` and `cdll` which uses FFI) to invoke the functions

## Getting Started

* Install `libimobiledevice` and its friends
    * macOS - `brew install libimobiledevice`
    * Debian / Ubuntu - `apt install libimobiledevice`
    * Some libraries are extra
* `pip install libimobiledevice`

## Hello iDevice

```
from libimobiledevice import *

```