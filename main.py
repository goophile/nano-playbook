#!/usr/bin/env python3

import os
import sys
import time
import threading

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_PATH)

from pico.libs.network import message_encode, message_decode, Network
from pico.libs.account import Account
from pico.libs.block import Block


KEEPALIVE_INTERVAL = 30
EMPTY_PEER = ('::', 0, 0, 0)
TEST_PEER1 = None
TEST_PEER2 = None
# TEST_PEER1 = ('::ffff:10.1.1.21', 7075, 0, 0)
# TEST_PEER2 = ('::ffff:10.1.1.22', 7075, 0, 0)


def network_receive(session):
    """
    Receive and process packets.
    """

    while True:
        block = None
        data = session.receive()
        message_type, block_type, representative_bytes, block_bytes = message_decode(data)

        if message_type == 'keepalive':
            peers_list = session.unpack_peers(block_bytes)
            print('got keepalive peers: %s' % peers_list)
            session.update_peers(peers_list)

        elif message_type in ['publish', 'confirm_ack', 'confirm_req']:
            if block_type in ['open', 'receive', 'send', 'change']:
                block = Block(type=block_type)
            else:
                print('unkonwn block_type: %s' % block_type)
        else:
            print('unkonwn message_type: %s' % message_type)

        if not block:
            continue

        block.from_network_bytes(block_bytes)
        block.hash = block.calculate_hash().hex()
        print('block hash: %s, work valid: %s, block type: %s' %
              (block.hash, block.work_valid(), block.type))


def network_keepalive(session):
    """
    Send keepalive packets periodically.
    """

    # first, send init packet with empty peers.
    empty_bytes = session.pack_peers(EMPTY_PEER)
    message_bytes = message_encode('keepalive', 'invalid', b'', empty_bytes)
    session.send(message_bytes, TEST_PEER1)

    while True:
        peers_bytes = session.pack_peers(TEST_PEER2)
        message_bytes = message_encode('keepalive', 'invalid', b'', peers_bytes)
        session.send(message_bytes, TEST_PEER1)
        time.sleep(KEEPALIVE_INTERVAL)


def main():
    session = Network()
    session.bind()

    workers = [network_receive, network_keepalive]
    daemons = []

    for worker in workers:
        t = threading.Thread(target=worker, args=(session, ))
        t.daemon = True
        t.start()
        daemons.append(t)

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()

