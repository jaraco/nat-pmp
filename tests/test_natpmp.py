import socket
import struct

import pytest

import natpmp


def test_public_address_request():
    request = natpmp.PublicAddressRequest()
    assert request.toBytes() == b'\x00\x00'


def test_port_map_request():
    request = natpmp.PortMapRequest(natpmp.NATPMP_PROTOCOL_TCP, 80, 8080)
    assert request.toBytes() == struct.pack('!BBHHHI', 0, 2, 0, 80, 8080, 3600)


def test_response_str():
    response = natpmp.NATPMPResponse(0, 128, 0, 42)
    assert str(response) == 'NATPMPResponse(0, 128, 0, 42)'


def test_public_address_response():
    data = struct.pack('!BBHI', 0, 128, 0, 42) + socket.inet_aton('192.0.2.1')
    response = natpmp.PublicAddressResponse(data)
    assert response.ip == '192.0.2.1'
    assert str(response) == (
        'PublicAddressResponse: version 0, opcode 128, result 0, ssec 42, ip 192.0.2.1'
    )


def test_port_map_response():
    data = struct.pack('!BBHIHHI', 0, 130, 0, 42, 80, 8080, 3600)
    response = natpmp.PortMapResponse(data)
    assert str(response) == (
        'PortMapResponse: version 0, opcode 130 (130), result 0, '
        'ssec 42, private_port 80, public port 8080, lifetime 3600'
    )


def test_read_response():
    left, right = socket.socketpair()
    with left, right:
        right.sendall(b'data')
        data, _ = natpmp.read_response(left, timeout=5)
    assert data == b'data'


class FailingSocket:
    def __init__(self, sock):
        self.sock = sock

    def fileno(self):
        return self.sock.fileno()

    def recvfrom(self, size):
        raise OSError("failed")


def test_read_response_error():
    left, right = socket.socketpair()
    with left, right:
        right.sendall(b'data')
        result = natpmp.read_response(FailingSocket(left), timeout=5)
    assert result == (None, None)


def test_forward_port_invalid():
    with pytest.raises(Exception, match="Invalid port"):
        natpmp.NatPMP().forward_port('tcp', 0, '192.0.2.1')
