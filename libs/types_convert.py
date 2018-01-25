#!/usr/bin/env python3

from bitstring import BitArray


def int_to_bytes(i, length=64):
    """
    Convert int to bytes, length is bit length.
    """
    if not isinstance(i, int):
        raise ValueError('int_to_bytes: data is not int')

    i_bits = BitArray(uint=i, length=length)
    return i_bits.tobytes()


def bytes_to_hex(b):
    """
    Convert bytes to hex string.
    """
    if not isinstance(b, bytes):
        raise ValueError('bytes_to_hex: data is not bytes')

    return b.hex()


def hex_to_bytes(h):
    """
    Convert hex string to bytes.
    """
    is_valid_hex(h, strict=True)
    return bytes.fromhex(h)


def hex_to_int(h):
    """
    Convert hex string to int.
    """
    is_valid_hex(h, strict=True)
    return int(h, 16)


def is_valid_hex(data, length=0, strict=False):
    """
    Check if a data is a hex string with given length (string length, not bytes length).
    If length=0, don't check length.
    If strict=True, raise Exception on False.
    """

    if _is_valid_hex(data, length):
        return True
    else:
        if strict:
            raise ValueError('data is not hex string or length not match')
        else:
            return False


def _is_valid_hex(string, length=0):

    if not isinstance(string, str):
        return False

    if length != 0 and len(string) != length:
        return False

    try:
        bytes.fromhex(string)
        return True
    except Exception:
        return False

