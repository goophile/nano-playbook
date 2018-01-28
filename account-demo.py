#!/usr/bin/env python3


from libs.account import *


test_seed        = 'CCC020CAF01C98B6B076A9F00573503E0D7FBA85BC7CA21AF3B3C02A2DDF5326'
test_address_0   = 'xrb_1ubrtesxophtmpqseazk397ec4eaffdzd3gapp1sb1c4qexzjjxppfqdhaer'
test_address_1   = 'xrb_17c51w1zn3ba46yb9jx5yn5proimw3h7p49pmokdry6yf366cok3rhrpff5c'
test_address_2   = 'xrb_318mhznow5ktgkh7qeuyzgwthkc7je5844898d8qosfbmsqwh843i8tp6d37'
test_address_3   = 'xrb_3hn6zrr4mdrqw4jgrpdxzoc4hwnnszf1hwet186tszsb7nnki5nu9wnes45b'
test_address_273 = 'xrb_39t9rkryf6wds9hbc5sr6ikg6y98ae7jzkgn6yj3tsz6dbrkrbxgco8fkdpb'
test_address_279 = 'xrb_3xmhjpbod4f6rcewn6qp7zxyu6xoohxzuaj9hgn5jsnzposcotfr6mhssk7z'


def seed_to_address(seed, index=0, debug=False):
    sk = seed_to_signing_key(seed, index)
    vk = signing_to_verifying_key(sk)
    addr = verifying_key_to_address(vk)
    if debug:
        print(sk.hex().upper())
        print(vk.hex().upper())
    return addr


print(seed_to_address(test_seed, 0, True))
print(seed_to_address(test_seed, 1234590123, True))

print(address_valid(test_address_1))
print(address_valid(test_address_2))
print(address_valid(test_address_273))


genesis_vk = bytes.fromhex('E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA')
genesis_addr = verifying_key_to_address(genesis_vk)
print(genesis_addr)

