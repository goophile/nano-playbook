#!/usr/bin/env python3

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from libs.network import message_encode, message_decode, Network

HEADER = '52430A0A07'

def test_message():
    # 144 bytes of data captured from network
    receive_block_hex = HEADER + '''030003
    6B6181C1AC75DAABD30CEAE15D44D30D238198968A5A794E057DC36503120550
    7716EF323E3079CF8BF9E7EFD1C40F60F8DD3251F24D3F455098EEA90A33572E
    3226710D0BD7D3E355F3F1D985AF8BA1B2EB9B346752DEF6F8C14C2C0E91C663A34B3F800E332E48913F7F1F65FF86342490B9C2F97D4FFF50B8F98ACD3DC90F
    86C3565BE806C52B
    '''

    network_hex_raw = ''.join(receive_block_hex.split())
    network_hex_block = ''.join(receive_block_hex.split()[1:])

    message_bytes = message_encode('publish', 'receive', b'', network_hex_block)
    assert message_bytes.hex().upper() == network_hex_raw

    message_type, block_type, vote_bytes, block_bytes = message_decode(network_hex_raw)
    assert message_type == 'publish'
    assert block_type == 'receive'
    assert vote_bytes == b''
    assert block_bytes.hex().upper() == network_hex_block


def test_message_with_vote():
    # 280 bytes of data captured from network
    open_block_hex = HEADER + '''050004
    E65294CF9E0192FE2E62E001F61806E7A207CD82B7005120F00EEABA2AC89E00
    440C3C58C57EB163C3ECC833F8CDBC1BA8CEF40DDF665506C9740D4F35E7E3E0FD743EC0371D46A81E6509CC7FEE154097F0AAF8C006FE8D8E47A3E02EADCB0F
    15D9A70400000000
    7B60805A2D681470CCBDEC381331C0DC3EA35451FEEED6FD6FB3E799D28A837D
    D95FEEEB8B08DA598821A72199141ED75D5860BCCB0CA4E041E1387207F9C993
    573113B6C57AB5877EC532F19E6C2F7CFD389C955FA5DDC9C03A35E29CB1632E
    B1D9B2E7FE5CF7CD5AD7CC18DB1F72225DED46527936A10E2E316CA114276021022BE9BB20D009770BF200BFACB18D53761D9B1CD2B8157D4AB96957AD155C0B
    55D10F0608FEE817
    '''

    network_hex_raw = ''.join(open_block_hex.split())
    network_hex_vote = ''.join(open_block_hex.split()[1:4])
    network_hex_block = ''.join(open_block_hex.split()[4:])

    message_bytes = message_encode('confirm_ack', 'open', network_hex_vote, network_hex_block)
    assert message_bytes.hex().upper() == network_hex_raw

    message_type, block_type, vote_bytes, block_bytes = message_decode(network_hex_raw)
    assert message_type == 'confirm_ack'
    assert block_type == 'open'
    assert vote_bytes.hex().upper() == network_hex_vote
    assert block_bytes.hex().upper() == network_hex_block


def test_message_keepalive():
    # 152 bytes of data captured from network
    keepalive_hex = HEADER + '''020000
    00000000000000000000ffffd57f36480545
    00000000000000000000ffff2578a7a4a31b
    00000000000000000000ffffc7f70194a31b
    00000000000000000000ffffad3826bea31b
    00000000000000000000ffff9f411985a31b
    00000000000000000000ffff5249a1afa31b
    00000000000000000000ffff48e4b0ffa31b
    00000000000000000000ffff5f553a18850d
    '''

    network_hex_raw = ''.join(keepalive_hex.split())
    network_hex_block = ''.join(keepalive_hex.split()[1:])

    message_bytes = message_encode('keepalive', 'invalid', b'', network_hex_block)
    assert message_bytes.hex().upper() == network_hex_raw.upper()

    message_type, block_type, vote_bytes, block_bytes = message_decode(network_hex_raw)
    assert message_type == 'keepalive'
    assert block_type == 'invalid'
    assert vote_bytes == b''
    assert block_bytes.hex().upper() == network_hex_block.upper()


def test_network_pack():
    # 152 bytes of data captured from network
    keepalive_hex = HEADER + '''020000
    00000000000000000000ffffd57f36480545
    00000000000000000000ffff2578a7a4a31b
    00000000000000000000ffffc7f70194a31b
    00000000000000000000ffffad3826bea31b
    00000000000000000000ffff9f411985a31b
    00000000000000000000ffff5249a1afa31b
    00000000000000000000ffff48e4b0ffa31b
    00000000000000000000ffff5f553a18850d
    '''

    network_hex_block = ''.join(keepalive_hex.split()[1:])
    session = Network()

    peers = session.unpack_peers(network_hex_block)
    peer = peers[3]  # choose one of them to check
    assert peer[1] == 7075

    keepalive_bytes = session.pack_peers(peers)
    assert keepalive_bytes.hex() == network_hex_block

    empty_peers = [('::', 0)]
    empty_bytes = session.pack_peers(empty_peers)
    assert empty_bytes.hex() == '0' * 18 * 8 * 2

