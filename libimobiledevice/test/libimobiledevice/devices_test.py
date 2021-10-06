#!/usr/bin/env python

from pytest import fixture
from pytest_describe import behaves_like
from libimobiledevice.device import Device


def describe_devices():
    def it_should_list_devices():
        devices = Device.devices()

    def it_should_open_a_device():
        devices = Device.devices()
        device = Device(devices[0])

    def it_should_get_device_info():
        devices = Device.devices()
        device = Device(devices[0])

        assert(device.udid == devices[0])