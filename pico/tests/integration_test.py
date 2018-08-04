#!/usr/bin/env python3

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from libs.account import Account, signing_to_verifying_key, verifying_key_to_address
from libs.block import Block
from libs.storage import Storage
from libs.network import Network, message_encode, message_decode
from libs.types_convert import to_bytes


my_signing_key = 'bdc8a8ef58200a401a85c10a9431282a4084f0cc9c527b546fa3aa5cafecbdb4'
my_verifying_key = signing_to_verifying_key(to_bytes(my_signing_key))
my_address = verifying_key_to_address(my_verifying_key)

my_account = Account(signing_key='bdc8a8ef58200a401a85c10a9431282a4084f0cc9c527b546fa3aa5cafecbdb4')


def test_integration_open(manual=False):
    open_block_hex = '''
    5243050501030004
    78D8D44D421C2C2B0DEE2DEA5DB3EBCA0D5EFED85835A85443FD64B69EB214C8
    AE7AC63990DAAAF2A69BF11C913B928844BF5012355456F2F164166464024B29
    966E5D2EA18F15F56BF18FB095D82C8A1B0F5C13428872A21AB7832B6C6E7F2A
    1686BD2016C05056394BEB6620804217A39EDE9925A476D900FF584D508236E5BE246A16712F7E702F647AD4C46E75EF0D38D9FEE5C27959AA7F57C667842204
    5EE2F0B881FE6122
    '''

    open_block_raw = ''.join(open_block_hex.split())

    open_block = Block(
            type            = "open",
            source          = "78D8D44D421C2C2B0DEE2DEA5DB3EBCA0D5EFED85835A85443FD64B69EB214C8",
            representative  = "xrb_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m",
            account         = my_address
        )

    open_block.hash = open_block.calculate_hash()
    open_block.signature = my_account.sign_block(open_block.hash)

    if manual:
        open_block.work = open_block.generate_work()
    else:
        open_block.work = '5EE2F0B881FE6122'

    assert my_account.signature_valid(open_block.hash, open_block.signature)
    assert open_block.work_valid()

    message_bytes = message_encode('publish', 'open', b'', open_block.to_network_bytes())
    if manual:
        print(open_block.hash.hex())
        return message_bytes
    else:
        assert message_bytes.hex().upper() == open_block_raw


def open_manual_with_network():
    udp_net = Network()
    udp_net.listen()
    message_bytes = test_integration_open(manual=True)
    print(message_bytes.hex())
    udp_net.send(message_bytes)


if __name__ == '__main__':
    print('uncomment to test manually')
    # open_manual_with_network()

