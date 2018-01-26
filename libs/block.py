#!/usr/bin/env python3


from pyblake2 import blake2b

from .types_convert import *
from .account import address_to_verifying_key, address_valid


class Block(object):

    def __init__(self, type,
            previous=None, source=None, destination=None, account=None, balance=None, representative=None,
            hash=None,signature=None, work=None):
        """
        This Class only store the 4 types of blocks and their fields.
        Verifying key can be calucated from address, it's in the _bytes field. Signing key is not stored here.
        """

        self.type           = type
        self.previous       = previous          # (send/receive/change): hash of previous block
        self.source         = source            # (open/receive): hash of the associated send block
        self.balance        = balance           # (send): a 128 bit integer, in raw unit
        self.destination    = destination       # (send): destination address of send transaction
        self.account        = account           # (open): address of the open account
        self.representative = representative    # (open/change): address of the representative

        # call _prepare_block() to convert to bytes
        self._previous_bytes       = None
        self._source_bytes         = None
        self._destination_bytes    = None
        self._account_bytes        = None
        self._representative_bytes = None
        self._balance_bytes        = None

        self.hash       = hash
        self.signature  = signature
        self.work       = work

    def _calculate_hash_open(self):
        """
        Calculate the hash of open block, return bytes.
        """

        if self._source_bytes is None or self._representative_bytes is None or self._account_bytes is None:
            raise Exception('can not calculate hash due to lack of fields')

        h = blake2b(digest_size=32)
        h.update(self._source_bytes)
        h.update(self._representative_bytes)
        h.update(self._account_bytes)
        return h.digest()

    def _calculate_hash_send(self):
        """
        Calculate the hash of send block, return bytes.
        """

        if self._previous_bytes is None or self._destination_bytes is None or self._balance_bytes is None:
            raise Exception('can not calculate hash due to lack of fields')

        h = blake2b(digest_size=32)
        h.update(self._previous_bytes)
        h.update(self._destination_bytes)
        h.update(self._balance_bytes)
        return h.digest()

    def _calculate_hash_receive(self):
        """
        Calculate the hash of receive block, return bytes.
        """

        if self._previous_bytes is None or self._source_bytes is None:
            raise Exception('can not calculate hash due to lack of fields')

        h = blake2b(digest_size=32)
        h.update(self._previous_bytes)
        h.update(self._source_bytes)
        return h.digest()

    def _calculate_hash_change(self):
        """
        Calculate the hash of change block, return bytes.
        """

        if self._previous_bytes is None or self._representative_bytes is None:
            raise Exception('can not calculate hash due to lack of fields')

        h = blake2b(digest_size=32)
        h.update(self._previous_bytes)
        h.update(self._representative_bytes)
        return h.digest()

    def _to_verifying_key(self, data):
        """
        Convert data to verifying key if legal, return bytes or None.
        """

        vk = to_bytes(data, 32)
        if vk is None and isinstance(data, str) and address_valid(data):
            vk = address_to_verifying_key(data)
        return vk

    def _to_block_hash(self, data):
        """
        Convert data to 32 bytes hash if legal, return bytes or None.
        """
        return to_bytes(data, 32)

    def _to_balance(self, data):
        """
        Convert data to 128-bits bytes if legal, return bytes or None.
        """

        balance = to_bytes(data, 16)
        if balance is None and isinstance(data, int):
            balance = int_to_bytes(data, 128)
        return balance

    def _prepare_block(self):
        """
        Convert all available fields to bytes.
        """

        self._previous_bytes = self._to_block_hash(self.previous)
        self._source_bytes = self._to_block_hash(self.source)

        self._balance_bytes = self._to_balance(self.balance)

        self._destination_bytes = self._to_verifying_key(self.destination)
        self._account_bytes = self._to_verifying_key(self.account)
        self._representative_bytes = self._to_verifying_key(self.representative)

    def calculate_hash(self):
        """
        Calculate block hash according to its type, return bytes.
        """

        # first, convert all fields to bytes.
        self._prepare_block()

        if self.type == 'open':
            return self._calculate_hash_open()

        elif self.type == 'send':
            return self._calculate_hash_send()

        elif self.type == 'receive':
            return self._calculate_hash_receive()

        elif self.type == 'change':
            return self._calculate_hash_change()

        else:
            raise ValueError('block type not defined')
