#!/usr/bin/env python3


from pyblake2 import blake2b
from bitstring import BitArray

from .pure25519 import ed25519_oop as ed25519
from .zbase32 import decode as b32_decode
from .zbase32 import encode as b32_encode
from .types_convert import *


class Account(object):

    def __init__(self, signing_key=None, verifying_key=None, address=None):
        """
        Create an account with signing_key that can sign/verify, or only verifying_key/address that can verify.
        No seed involved, so one Account can hold only one signing key.
        """
        self.signing_key    = signing_key
        self.verifying_key  = verifying_key
        self.address        = address

        self._signing_key_bytes     = None
        self._verifying_key_bytes   = None

    def _to_signing_key(self, data):
        """
        Convert data to signing key if legal, return bytes or None.
        """

        return to_bytes(data, 32)

    def _to_verifying_key(self, data):
        """
        Convert data to verifying key if legal, return bytes or None.
        """

        vk = to_bytes(data, 32)
        if vk is None and isinstance(data, str) and address_valid(data):
            vk = address_to_verifying_key(data)
        return vk

    def _prepare_account(self):
        """
        If signing_key is given, generate verifying_key/address from signing_key.
        If not, generate address/verifying_key from each other.
        """

        if self.signing_key is None and self.verifying_key is None and self.address is None:
            raise Exception('signing_key/verifying_key/address, must give at least one')

        signing_key_bytes = self._to_signing_key(self.signing_key)
        verifying_key_bytes = self._to_verifying_key(self.verifying_key)
        address_bytes = self._to_verifying_key(self.address)

        if signing_key_bytes is not None:
            _verifying_key_bytes = signing_to_verifying_key(signing_key_bytes)

            # Guard against signing_key/verifying_key/address mismatch.
            if verifying_key_bytes is not None and _verifying_key_bytes != verifying_key_bytes:
                raise Exception('signing_key and verifying_key not match')
            if address_bytes is not None and _verifying_key_bytes != address_bytes:
                raise Exception('signing_key and address not match')

            self._signing_key_bytes = signing_key_bytes
            self._verifying_key_bytes = _verifying_key_bytes

        else:

            if verifying_key_bytes is not None:
                if address_bytes is not None and verifying_key_bytes != address_bytes:
                    raise Exception('verifying_key and address not match')
                self._verifying_key_bytes = verifying_key_bytes

            elif address_bytes is not None:
                if verifying_key_bytes is not None and verifying_key_bytes != address_bytes:
                    raise Exception('verifying_key and address not match')
                self._verifying_key_bytes = address_bytes

    def sign_block(self, block_hash):
        self._prepare_account()
        if self._signing_key_bytes is None:
            raise Exception('can not sign block since signing_key is not given')

        hash_bytes = to_bytes(block_hash, 32, strict=True)

        sk_obj = ed25519.SigningKey(self._signing_key_bytes)
        return sk_obj.sign(hash_bytes)

    def signature_valid(self, block_hash, signature):
        """
        Use verifying key to verify block hash and the signature, return True or False
        """
        self._prepare_account()
        if self._verifying_key_bytes is None:
            raise Exception('can not verify block since verifying_key or address is not given')

        hash_bytes = to_bytes(block_hash, 32, strict=True)
        signature_bytes = to_bytes(signature, 64, strict=True)

        vk_obj = ed25519.VerifyingKey(self._verifying_key_bytes)
        try:
            vk_obj.verify(signature_bytes, hash_bytes)
            return True
        except:
            return False


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

