from libimobiledevice.afc import AfcClient
from libimobiledevice.device import Device


def describe_afc():
    device = Device('3ac82354b0a59ba46a03e8ae4937617063e26647')

    def it_should_create_a_client():
        client = AfcClient(device=device)
