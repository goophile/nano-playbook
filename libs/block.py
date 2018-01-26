#!/usr/bin/env python3


import os
from pyblake2 import blake2b

from .types_convert import *
from .account import address_to_verifying_key, address_valid

POW_THRESHOLD = bytes.fromhex('FFFFFFC000000000')


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

        h = blake2b(digest_size=32)
        h.update(self._source_bytes)
        h.update(self._representative_bytes)
        h.update(self._account_bytes)
        return h.digest()

    def _calculate_hash_send(self):
        """
        Calculate the hash of send block, return bytes.
        """

        h = blake2b(digest_size=32)
        h.update(self._previous_bytes)
        h.update(self._destination_bytes)
        h.update(self._balance_bytes)
        return h.digest()

    def _calculate_hash_receive(self):
        """
        Calculate the hash of receive block, return bytes.
        """

        h = blake2b(digest_size=32)
        h.update(self._previous_bytes)
        h.update(self._source_bytes)
        return h.digest()

    def _calculate_hash_change(self):
        """
        Calculate the hash of change block, return bytes.
        """

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

        self._validate_fields()

    def _validate_fields(self):
        """
        Validate block type and its fields.
        """

        if self.type == 'open':
            if None in [self._source_bytes, self._representative_bytes, self._account_bytes]:
                raise Exception('block lack of fields')

        elif self.type == 'send':
            if None in [self._previous_bytes, self._destination_bytes, self._balance_bytes]:
                raise Exception('block lack of fields')

        elif self.type == 'receive':
            if None in [self._previous_bytes, self._source_bytes]:
                raise Exception('block lack of fields')

        elif self.type == 'change':
            if None in [self._previous_bytes, self._representative_bytes]:
                raise Exception('block lack of fields')

        else:
            raise ValueError('wrong block type: %s' % self.type)

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

    def work_valid(self):
        self._prepare_block()

        if self.type == 'open':
            field_bytes = self._account_bytes
        else:
            field_bytes = self._previous_bytes

        work_bytes = to_bytes(self.work, 8)

        return self._work_valid(work_bytes, field_bytes)

    def _work_valid(self, work_bytes, field_bytes):
        work_bytes = bytearray(work_bytes)
        work_bytes.reverse()

        h = blake2b(digest_size=8)
        h.update(work_bytes)
        h.update(field_bytes)

        hash_bytes = bytearray(h.digest())
        hash_bytes.reverse()

        return hash_bytes > POW_THRESHOLD

    def generate_work(self):
        """
        Compute a nonce such that the hash of the nonce concatenated with the field is below a threshold.
        For open block, the field is the account. For other blocks, the field is the previous block.
        """

        self._prepare_block()
        if self.type == 'open':
            field_bytes = self._account_bytes
        else:
            field_bytes = self._previous_bytes

        i = 0
        work_bytes = os.urandom(8)
        while self._work_valid(work_bytes, field_bytes) is False:
            i += 1
            work_bytes = os.urandom(8)

        print('guess round for a valid work: %d' % i)
        return work_bytes

