#!/usr/bin/env python3

import lmdb
import os

from .types_convert import to_bytes

HOME_DIR = os.path.expanduser('~')
DEFAULT_DB_DIR = os.path.join(HOME_DIR, 'RaiBlocks')
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, 'data.ldb')


# tables in my desktop wallet database, got with env.begin(db=None)
_db_name_list_example = [
    (b'2CC17778107A1907AE00468C509443F40E32E4D23F2098D816E205969CC26966', '00000000000002000100000000000000090000000000000000000000000000002001000000000000c3c3000000000000'),
    (b'accounts', '00000000000003000c000000000000004c020000000000000000000000000000e01e000000000000bd05000000000000'),
    (b'blocks_info', '00000000000003000500000000000000fd000000000000000000000000000000991e000000000000731e000000000000'),
    (b'change', '0000000000000200010000000000000022000000000000000000000000000000c201000000000000987b030000000000'),
    (b'checksum', '00000000000001000000000000000000010000000000000000000000000000000100000000000000a29d010000000000'),
    (b'frontiers', '00000000000003000500000000000000d9000000000000000000000000000000e01e000000000000440a000000000000'),
    (b'meta', '000000000000010000000000000000000100000000000000000000000000000001000000000000000300000000000000'),
    (b'open', '00000000000003000a00000000000000cb020000000000000000000000000000e01e000000000000fd03000000000000'),
    (b'pending', '0000000000000400900000000000000076020000000000000000000000000000b8200000000000000c03000000000000'),
    (b'receive', '00000000000004009800000000000000352c00000000000000000000000000002e3a0200000000005f0b000000000000'),
    (b'representation', '0000000000000200010000000000000006000000000000000000000000000000f200000000000000b207000000000000'),
    (b'send', '0000000000000400e200000000000000a7330000000000000000000000000000c5790200000000009207000000000000'),
    (b'unchecked', '00000000040004001314000000000000ee80050000000000000000000000000030ab4800000000005361010000000000'),
    (b'unsynced', '00000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffffffffffff'),
    (b'vote', '000000000000020001000000000000002f000000000000000000000000000000b801000000000000e494010000000000'),
]


class Storage(object):

    def __init__(self, db_path=DEFAULT_DB_PATH, readonly=True):
        self.db_path            = db_path
        self.readonly           = readonly
        self.env                = lmdb.open(db_path, subdir=False, readonly=readonly, max_dbs=128)
        self._db_handle_dict    = {}

    def _to_db_name(self, db_name):
        if isinstance(db_name, (bytes, bytearray)):
            db_name = bytes(db_name)
        elif isinstance(db_name, str):
            db_name = db_name.encode()
        return db_name

    def _get_db_names(self):
        """
        return the names of all databases/tables.
        """

        db_names = []
        with self.env.begin() as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                db_names.append(key)

        return db_names

    def _get_db_handle(self, db_name):
        """
        open named db and store the handles in a dict to avoid too much open actions.
        """

        db_name = self._to_db_name(db_name)
        if db_name not in self._db_handle_dict:
            db_handle = self.env.open_db(db_name)
            self._db_handle_dict[db_name] = db_handle

        return self._db_handle_dict[db_name]

    def _put_data(self, db_name, key_bytes, data_bytes):
        """
        if db_name does not exist, create the db.
        """

        db = self._get_db_handle(db_name)
        with self.env.begin(db=db, write=True) as txn:
            txn.put(key_bytes, data_bytes)

    def _get_data(self, db_name, key_bytes):
        db = self._get_db_handle(db_name)

        with self.env.begin(db=db) as txn:
            cursor = txn.cursor()
            return cursor.get(key_bytes)

    def _to_block_hash_bytes(self, data):
        """
        Convert data to 32 bytes hash if legal, return bytes.
        """

        return to_bytes(data, 32)

    def put_block(self, block_type, block_hash, data):
        """
        block_type as db name, block_hash as key.
        if called twice with the same block_hash, the last data will overwrite the previous one.
        """

        block_hash_bytes = self._to_block_hash_bytes(block_hash)
        if isinstance(data, (bytes, bytearray)):
            data_bytes = bytes(data)
        else:
            raise ValueError('data is not bytes')

        self._put_data(block_type, block_hash_bytes, data)

    def get_block(self, block_type, block_hash):
        block_hash_bytes = self._to_block_hash_bytes(block_hash)
        return self._get_data(block_type, block_hash_bytes)

    def _get_block_all_db(self, block_hash):
        """
        for debug purpose: get all blocks in all db with the same hash.
        """

        db_list = self._get_db_names()
        db_dict = {}
        for db_name in db_list:
            data = self.get_block(db_name, block_hash)
            db_dict[db_name] = data

        return db_dict

    def _search_db(self, db_name, data):
        """
        for debug purpose: search key and value for the data, in a single db.
        """

        db = self._get_db_handle(db_name)
        with self.env.begin(db=db) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                if data in key or data in value:
                    return key, value

        return None, None

    def _search_all_db(self, data):
        """
        for debug purpose: search key and value for the data, in all db.
        """

        db_list = self._get_db_names()
        db_dict = {}
        for db_name in db_list:
            key, value = self._search_db(db_name, data)
            if key:
                db_dict[db_name] = (key.hex(), value.hex())

        return db_dict

    def _get_db_size(self, db_name):
        """
        for debug purpose: return how many items are there in the table.
        """

        cnt = 0
        db = self._get_db_handle(db_name)
        with self.env.begin(db=db) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                cnt += 1

        return cnt

