#!/usr/bin/env python3

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from libs.account import *


GENESIS_ADDRESS = 'xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3'

# These address were generated with the desktop wallet.
GLOBAL_SEED         = 'CCC020CAF01C98B6B076A9F00573503E0D7FBA85BC7CA21AF3B3C02A2DDF5326'
GLOBAL_ADDRESS_0    = 'xrb_1ubrtesxophtmpqseazk397ec4eaffdzd3gapp1sb1c4qexzjjxppfqdhaer'
GLOBAL_ADDRESS_1    = 'xrb_17c51w1zn3ba46yb9jx5yn5proimw3h7p49pmokdry6yf366cok3rhrpff5c'
GLOBAL_ADDRESS_2    = 'xrb_318mhznow5ktgkh7qeuyzgwthkc7je5844898d8qosfbmsqwh843i8tp6d37'
GLOBAL_ADDRESS_3    = 'xrb_3hn6zrr4mdrqw4jgrpdxzoc4hwnnszf1hwet186tszsb7nnki5nu9wnes45b'
GLOBAL_ADDRESS_273  = 'xrb_39t9rkryf6wds9hbc5sr6ikg6y98ae7jzkgn6yj3tsz6dbrkrbxgco8fkdpb'
GLOBAL_ADDRESS_279  = 'xrb_3xmhjpbod4f6rcewn6qp7zxyu6xoohxzuaj9hgn5jsnzposcotfr6mhssk7z'


def test_seed_to_address_0():
    seed = GLOBAL_SEED
    index = 0
    sk = seed_to_signing_key(seed, index)
    vk = signing_to_verifying_key(sk)
    addr = verifying_key_to_address(vk)
    assert addr == GLOBAL_ADDRESS_0


def test_seed_to_address_279():
    seed = GLOBAL_SEED
    index = 279
    sk = seed_to_signing_key(seed, index)
    vk = signing_to_verifying_key(sk)
    addr = verifying_key_to_address(vk)
    assert addr == GLOBAL_ADDRESS_279


def test_address_to_verifying_key():
    genesis_verifying_key = 'E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA'
    assert address_to_verifying_key(GENESIS_ADDRESS).hex().upper() == genesis_verifying_key


def test_address_valid():
    assert address_valid(GLOBAL_ADDRESS_0)
    assert address_valid(GLOBAL_ADDRESS_1)
    assert address_valid(GLOBAL_ADDRESS_2)
    assert address_valid(GLOBAL_ADDRESS_3)
    assert address_valid(GLOBAL_ADDRESS_273)
    assert address_valid(GLOBAL_ADDRESS_279)
    genesis_account = Account(address=GENESIS_ADDRESS)
    assert genesis_account.address_valid


def test_address_invalid():
    # modify GLOBAL_ADDRESS_1 a little bit
    illegal_address = 'xrb_17c51w1zn3ba46yb9jx5yn5proimw3h7p49pmokdry6yf366cok3rhrpff51'
    illegal_account = Account(address=illegal_address)
    assert illegal_account.address_valid == False


def test_address_to_xrb():
    genesis_verifying_key = 'E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA'
    genesis_account = Account(address=genesis_verifying_key)
    assert genesis_account.xrb_address == GENESIS_ADDRESS


def test_account_signature():
    genesis_account = Account(address=GENESIS_ADDRESS)
    genesis_block_hash = '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'
    signature = '9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02'
    assert genesis_account.signature_valid(genesis_block_hash, signature)


if __name__ == '__main__':
    account = Account(address='E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA')
    print(account)

