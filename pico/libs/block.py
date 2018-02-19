#!/usr/bin/env python3


import os
from pyblake2 import blake2b

from .types_convert import to_bytes, int_to_bytes
from .account import address_to_verifying_key, address_valid


POW_THRESHOLD = bytes.fromhex('FFFFFFC000000000')
GENESIS_HASH = bytes.fromhex('991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948')
EMPTY_HASH = '0000000000000000000000000000000000000000000000000000000000000000'


class Block(object):

    def __init__(self, type,
            previous=None, source=None,
            balance=None,
            destination=None, account=None, representative=None,
            signature=None, work=None, hash=None,
            next=EMPTY_HASH):
        """
        This Class only stores the 4 types of blocks and their fields.
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

        self.signature  = signature
        self.work       = work
        self.hash       = hash
        self.next       = next

        self._signature_bytes = None
        self._work_bytes      = None
        self._hash_bytes      = None
        self._next_bytes      = None

        self._is_genesis = False

    def __str__(self):
        """
        Reture a readable hex string of the hash.
        """
        if self.hash:
            return self.hash
        else:
            return self.calculate_hash().hex().upper()

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
        Convert data to verifying key if legal, return bytes.
        """

        vk = to_bytes(data, 32)
        if not vk and isinstance(data, str) and address_valid(data):
            vk = address_to_verifying_key(data)
        return vk

    def _to_balance(self, data):
        """
        Convert data to 128-bits bytes if legal, return bytes.
        """

        balance = to_bytes(data, 16)
        if not balance and isinstance(data, int):
            balance = int_to_bytes(data, 128)
        return balance

    def _prepare_block(self):
        """
        Convert all available fields to bytes.
        """

        self._previous_bytes = to_bytes(self.previous, 32)
        self._source_bytes = to_bytes(self.source, 32)

        self._balance_bytes = self._to_balance(self.balance)

        self._destination_bytes = self._to_verifying_key(self.destination)
        self._account_bytes = self._to_verifying_key(self.account)
        self._representative_bytes = self._to_verifying_key(self.representative)

        self._signature_bytes = to_bytes(self.signature, 64)
        self._work_bytes = to_bytes(self.work, 8)
        self._next_bytes = to_bytes(self.work, 32)

    def _validate_fields(self):
        """
        Validate block type and its fields.
        """

        if self.type == 'open':
            if not (self._source_bytes and self._representative_bytes and self._account_bytes):
                raise Exception('block lack of fields')

        elif self.type == 'send':
            if not (self._previous_bytes and self._destination_bytes and self._balance_bytes):
                raise Exception('block lack of fields')

        elif self.type == 'receive':
            if not (self._previous_bytes and self._source_bytes):
                raise Exception('block lack of fields')

        elif self.type == 'change':
            if not (self._previous_bytes and self._representative_bytes):
                raise Exception('block lack of fields')

        else:
            raise ValueError('wrong block type: %s' % self.type)

    def calculate_hash(self):
        """
        Calculate block hash according to its type, return bytes.
        """

        # first, convert all fields to bytes.
        self._prepare_block()
        self._validate_fields()

        if self.type == 'open':
            self._hash_bytes = self._calculate_hash_open()

        elif self.type == 'send':
            self._hash_bytes = self._calculate_hash_send()

        elif self.type == 'receive':
            self._hash_bytes = self._calculate_hash_receive()

        elif self.type == 'change':
            self._hash_bytes = self._calculate_hash_change()

        if self._hash_bytes == GENESIS_HASH:
            self._is_genesis = True

        return self._hash_bytes

    def work_valid(self):
        self._prepare_block()

        if self.type == 'open':
            field_bytes = self._account_bytes
        else:
            field_bytes = self._previous_bytes

        return self._work_valid(self._work_bytes, field_bytes)

    def _work_valid(self, work_bytes, field_bytes):
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

    def _pack(self):
        """
        Pack a Block class to continuous bytes.
        Packed fields: hash-fields, signature and work.
        """

        self._prepare_block()
        self._validate_fields()

        if not self._signature_bytes:
            raise ValueError('can not pack with a None signature')

        if not self.work_valid():
            raise ValueError('can not pack with a invalid work: %s' % self.work)

        packed_bytes = b''

        if self.type == 'open':
            packed_bytes = self._source_bytes + self._representative_bytes + self._account_bytes

        elif self.type == 'send':
            packed_bytes = self._previous_bytes + self._destination_bytes + self._balance_bytes

        elif self.type == 'receive':
            packed_bytes = self._previous_bytes + self._source_bytes

        elif self.type == 'change':
            packed_bytes = self._previous_bytes + self._representative_bytes

        packed_bytes += self._signature_bytes
        packed_bytes += self._work_bytes

        return packed_bytes

    def _unpack(self, packed_bytes):
        """
        Reverse the _pack().
        """

        if self.type == 'open':
            if len(packed_bytes) != 168:
                raise Exception('invalid data length to unpack: %s' % len(packed_bytes))

            self.source = packed_bytes[0:32]
            self.representative = packed_bytes[32:64]
            self.account = packed_bytes[64:96]
            self.signature = packed_bytes[96:160]
            self.work = packed_bytes[160:168]

        elif self.type == 'send':
            if len(packed_bytes) != 152:
                raise Exception('invalid data length to unpack: %s' % len(packed_bytes))

            self.previous = packed_bytes[0:32]
            self.destination = packed_bytes[32:64]
            self.balance = packed_bytes[64:80]
            self.signature = packed_bytes[80:144]
            self.work = packed_bytes[144:152]

        elif self.type == 'receive':
            if len(packed_bytes) != 136:
                raise Exception('invalid data length to unpack: %s' % len(packed_bytes))

            self.previous = packed_bytes[0:32]
            self.source = packed_bytes[32:64]
            self.signature = packed_bytes[64:128]
            self.work = packed_bytes[128:136]

        elif self.type == 'change':
            if len(packed_bytes) != 136:
                raise Exception('invalid data length to unpack: %s' % len(packed_bytes))

            self.previous = packed_bytes[0:32]
            self.representative = packed_bytes[32:64]
            self.signature = packed_bytes[64:128]
            self.work = packed_bytes[128:136]

        else:
            raise ValueError('wrong block type: %s' % self.type)

    def to_network_bytes(self):
        """
        TODO: In the captured packets, some blocks have 3 previous fields,
        still unknown what they are, so don't handle them for now.
        """
        return self._pack()

    def to_storage_bytes(self):
        packed_bytes = self._pack()
        next_bytes = to_bytes(self.next, 32)
        packed_bytes += next_bytes
        return packed_bytes

    def from_network_bytes(self, data):
        """
        Should pass sliced data from network (remove `type` field and the 3 previous fields in packets.)
        """
        packed_bytes = to_bytes(data)
        self._unpack(packed_bytes)

    def from_storage_bytes(self, data):
        packed_bytes = to_bytes(data)
        self._next_bytes = packed_bytes[-32:]
        self._unpack(packed_bytes[:-32])

