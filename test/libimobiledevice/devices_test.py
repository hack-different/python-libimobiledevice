from libimobiledevice.device import Device


def describe_devices():
    def it_should_open_a_device():
        device = Device('3ac82354b0a59ba46a03e8ae4937617063e26647')

    def it_should_get_device_info():
        device = Device('3ac82354b0a59ba46a03e8ae4937617063e26647')

        assert(device.udid == b'3ac82354b0a59ba46a03e8ae4937617063e26647')