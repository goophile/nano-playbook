#!/usr/bin/env python3

import socket 
import random

from .types_convert import *


PRECONFIGURED_PEERS = [
        ("rai.raiblocks.net", 7075),
        ]

TEST_PEER = '10.1.1.1'

# rai/node/common.hpp (85n): enum class message_type : uint8_t
MESSAGE_TYPE_HEX_DICT = {
    '00' : 'invalid',
    '01' : 'not_a_type',
    '02' : 'keepalive',
    '03' : 'publish',
    '04' : 'confirm_req',
    '05' : 'confirm_ack',
    '06' : 'bulk_pull',
    '07' : 'bulk_push',
    '08' : 'frontier_req',
    '09' : 'bulk_pull_blocks',
}

MESSAGE_TYPE_DICT = {
    'invalid'           : '00',
    'not_a_type'        : '01',
    'keepalive'         : '02',
    'publish'           : '03',
    'confirm_req'       : '04',
    'confirm_ack'       : '05',
    'bulk_pull'         : '06',
    'bulk_push'         : '07',
    'frontier_req'      : '08',
    'bulk_pull_blocks'  : '09',
}

# rai/lib/blocks.hpp (32n): enum class block_type : uint8_t
BLOCK_TYPE_HEX_DICT = {
    '00' : 'invalid',
    '01' : 'not_a_block',
    '02' : 'send',
    '03' : 'receive',
    '04' : 'open',
    '05' : 'change',
}

BLOCK_TYPE_DICT = {
    'invalid'       : '00',
    'not_a_block'   : '01',
    'send'          : '02',
    'receive'       : '03',
    'open'          : '04',
    'change'        : '05',
}

STREAM_A        = '52'
STREAM_B        = '43'
VERSION_MAX     = '05'
VERSION_USING   = '05'
VERSION_MIN     = '01'
EXTENSION       = '00'

_header_hex_example = '52 43 05 05 01 03 00 03'


LOCAL_HEADER_PREFIX  = [STREAM_A, STREAM_B, VERSION_MAX, VERSION_USING, VERSION_MIN, ]
REPRESENTATIVE_DATA_LEN = 104 # bytes


def message_encode(message_type, block_type, representative_data, block_data):
    """
    Encode Block packed data into network message.
    representative_data may be empty.
    """
    representative_bytes = to_bytes(representative_data)
    block_bytes = to_bytes(block_data)

    message_type = MESSAGE_TYPE_DICT[message_type]
    block_type = BLOCK_TYPE_DICT[block_type]

    header_hex = ''.join(LOCAL_HEADER_PREFIX + [message_type, EXTENSION, block_type])
    header_bytes = to_bytes(header_hex)

    message_bytes = header_bytes + representative_bytes + block_bytes
    return message_bytes


def message_decode(message):
    """
    Decode network message into representative data and Block packed data.
    """
    message_bytes = to_bytes(message)
    header_bytes = message_bytes[0:8]

    header_hex = [int_to_bytes(b, 8).hex() for b in header_bytes]
    (stream_a, stream_b, version_max, version_using, version_min, message_type, extension, block_type) = header_hex

    message_type = MESSAGE_TYPE_HEX_DICT[message_type]
    block_type = BLOCK_TYPE_HEX_DICT[block_type]

    if message_type == 'confirm_ack':
        representative_bytes = message_bytes[8: 8+REPRESENTATIVE_DATA_LEN]
        block_bytes = message_bytes[8+REPRESENTATIVE_DATA_LEN:]
    else:
        representative_bytes = b''
        block_bytes = message_bytes[8:]

    return message_type, block_type, representative_bytes, block_bytes


class Network(object):
    """
    Send/Receive packets.
    """
    def __init__(self, ip='0.0.0.0', peering_port=7075):
        self.ip                 = ip
        self.peering_port       = peering_port
        self._peering_session   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_set           = set(PRECONFIGURED_PEERS) # a list of peer addr (ip, port)

    def listen(self):
        self._peering_session.bind((self.ip, self.peering_port))

    def receive(self):
        data, addr = self._peering_session.recvfrom(1500)
        self.peer_set.add(addr)
        return data

    def send(self, data, address=None):
        # (ip, port) = random.choice(list(self.peer_set))
        if address:
            self._peering_session.sendto(data, address)
        else:
            for addr in self.peer_set:
                self._peering_session.sendto(data, addr)

