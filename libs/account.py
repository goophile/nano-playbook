#!/usr/bin/env python3


from pyblake2 import blake2b
from bitstring import BitArray

from .pure25519 import ed25519_oop as ed25519
from .zbase32 import decode as b32_decode
from .zbase32 import encode as b32_encode


def seed_to_signing_key(seed, index=0):
    """
    from raiblocks seed to private key (ed25519 seed)

    :param str seed: the hex string of raiblocks seed, 64 characters long
    :param int index: the index of wallet address

    :rtype: bytes
    :return: signing key

    Code Example::

        seed = 'CCC020CAF01C98B6B076A9F00573503E0D7FBA85BC7CA21AF3B3C02A2DDF5326'
        sk = seed_to_signing_key(seed, 1)
        print(sk.hex())

    """

    h = blake2b(digest_size=32)

    seed_bytes = bytes.fromhex(seed)
    h.update(seed_bytes)

    index_bits = BitArray(uint=index, length=32)
    index_bytes = index_bits.tobytes()

    h.update(index_bytes)

    return h.digest()


def signing_to_verifying_key(sk):
    """
    ed25519 signing key to verifying key

    :param bytes sk: signing key

    :rtype: bytes
    :return: verifying key

    """

    sk_obj = ed25519.SigningKey(sk)
    vk_obj = sk_obj.get_verifying_key()
    return vk_obj.to_bytes()


def verifying_key_to_address(vk):
    """
    ed25519 verifying key to raiblocks address

    :param bytes vk: verifying key

    :rtype: str
    :return: raiblocks address

    """

    addr_b32 = b32_encode(vk)

    addr_checksum = bytearray(blake2b(vk, digest_size=5).digest())
    addr_checksum.reverse()
    checksum_b32 = b32_encode(addr_checksum)

    address = 'xrb_' + addr_b32 + checksum_b32
    return address


def address_to_verifying_key(address):
    """
    raiblocks address to ed25519 verifying key

    :param str address: raiblocks address

    :rtype: bytes
    :return: ed25519 verifying key

    """

    addr_b32 = address[4:56]
    vk = b32_decode(addr_b32)
    return vk


def address_valid(address):
    vk = address_to_verifying_key(address)
    new_addr = verifying_key_to_address(vk)

    if address == new_addr:
        return True
    else:
        return False

