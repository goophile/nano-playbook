#!/usr/bin/env python3


from bitstring import BitArray


ALPTHABET = "13456789abcdefghijkmnopqrstuwxyz"


def encode(data, padding_at_begin=True):
    """
    bytes data to base32 encoded string
    """
    if not isinstance(data, (bytes, bytearray)):
        data = bytes(data, 'utf-8')

    bit_array = BitArray()
    for b in bytes(data):
        bit_array.append(BitArray(uint=b, length=8))

    # padding: round bit_array length to multiple of 5 bits
    penny = len(bit_array) % 5
    if penny > 0:
        bit_array.append(BitArray(uint=0, length=(5-penny)))
        if padding_at_begin:
            bit_array.ror(5-penny)

    result = ''
    a, b = 0, 5
    while a < len(bit_array):
        b32_char = bit_array[a:b]
        result += ALPTHABET[b32_char.int]
        a, b = a+5, b+5

    return result


def decode(data, padding_at_begin=True):
    """
    base32 encoded string to bytes data
    """

    if not isinstance(data, str):
        raise Exception('decode error: only string accepted.')

    bit_array = BitArray()
    for s in data:
        if s in ALPTHABET:
            i = ALPTHABET.find(s)
            bit_array.append(BitArray(uint=i, length=5))
        else:
            raise Exception('decode error: char not in the ALPTHABET list: %s' % s)

    # remove padding 0 bits
    padding = len(bit_array) % 8
    if padding > 0:
        if padding_at_begin:
            bit_array.rol(padding)
        pad_char = bit_array[-padding:]
        if(pad_char.int > 0):
            raise Exception('decode error: none zero padding')
        bit_array = bit_array[:len(bit_array)-padding]

    bytes_data = bit_array.bytes

    return bytes_data

