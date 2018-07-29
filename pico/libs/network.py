#!/usr/bin/env python3

import socket
import random
import ipaddress

from .types_convert import to_bytes, int_to_bytes, hex_to_int, bytes_to_hex

# nslookup rai.raiblocks.net, got these peers
PRECONFIGURED_PEERS = [
        ('::ffff:192.99.176.122',  7075, 0, 0),
        ('::ffff:139.162.199.142', 7075, 0, 0),
        ('::ffff:144.217.167.119', 7075, 0, 0),
        ('::ffff:192.95.57.248',   7075, 0, 0),
        ('::ffff:192.99.176.121',  7075, 0, 0),
        ('::ffff:138.68.2.234',    7075, 0, 0),
        ('::ffff:138.201.94.249',  7075, 0, 0),
        ('::ffff:45.32.246.108',   7075, 0, 0),
        ('::ffff:128.199.199.97',  7075, 0, 0),
    ]

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

# rai/node/common.hpp (119n): static std::array<uint8_t, 2> constexpr magic_number
# rai_test_network: R A (5241)
# rai_beta_network: R B (5242)
# rai_live_network: R C (5243)
MAGIC_A         = '52'  # ascii of 'R'
MAGIC_B         = '43'  # ascii of 'C'
VERSION_MAX     = '05'
VERSION_USING   = '05'
VERSION_MIN     = '01'
EXTENSION       = '00'

_header_hex_example = '52 43 05 05 01 03 00 03'


LOCAL_HEADER_PREFIX  = [MAGIC_A, MAGIC_B, VERSION_MAX, VERSION_USING, VERSION_MIN, ]
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
    (magic_a, magic_b, version_max, version_using, version_min, message_type, extension, block_type) = header_hex

    if magic_a != MAGIC_A or magic_b != MAGIC_B:
        return None, None, None, None

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
    def __init__(self, ip='::', peering_port=7075):
        if ':' in ip:
            self.ip = ip  # IPv6
        else:
            self.ip = '::ffff:%s' % ip  # convert to IPv6-mapped-IPv4-address
        self.peering_port = peering_port
        self.peer_set = set(PRECONFIGURED_PEERS)  # a list of peer addr (ip, port)
        self._peering_session = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self._peering_session.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)

    def bind(self):
        self._peering_session.bind((self.ip, self.peering_port))

    def receive(self):
        data, addr = self._peering_session.recvfrom(1500)
        self.peer_set.add(addr)
        return data

    def send(self, data, address=None):
        """
        address is (ip, port) tupple pair.
        """
        data_bytes = to_bytes(data)

        if address:
            self._peering_session.sendto(data_bytes, address)
            return

        peer_list = list(self.peer_set)
        random.shuffle(peer_list)

        # TODO: should only send to a fixed list of peers
        for addr in peer_list[0:40]:
            try:
                self._peering_session.sendto(data_bytes, addr)
            except Exception as e:
                print('%s: unable to sendto %s' % (e, addr))

    def update_peers(self, peers):
        """
        Add peers to peer_set.
        """
        if isinstance(peers, (list, set)):
            peers = list(peers)
        elif isinstance(peers, str):
            peers = [peers, ]
        else:
            peers = []

        new_set = set()
        for peer in peers:
            if isinstance(peer, tuple) and '::ffff:' in str(peer[0]):  # TODO: only handle IPv4 for now
                new_set.add(peer)

        self.peer_set.update(new_set)

    def pack_peers(self, peers=None):
        """
        Select 8 random peers and pack to keepalive bytes.
        """

        if isinstance(peers, (list, set)):
            peers = list(peers)[0:8]
        elif isinstance(peers, str):
            peers = [peers, ]
        else:
            peer_list = list(self.peer_set)
            random.shuffle(peer_list)
            peers = peer_list[0:8]
            peers += [('::', 0)] * (8 - len(peers))  # append zeros to fit 8 peers length
        packed_bytes = b''
        for peer in peers:
            ip_bytes = ipaddress.IPv6Address(peer[0]).packed
            port_bytes = int_to_bytes(socket.htons(peer[1]), 16)
            packed_bytes += ip_bytes
            packed_bytes += port_bytes

        return packed_bytes

    def unpack_peers(self, packed_bytes):
        """
        Unpack keepalive bytes to peer address tuples.
        """

        packed_bytes = to_bytes(packed_bytes)
        packed_bytes += b'0' * (144 - len(packed_bytes))
        peer_bytes_list = []
        for i in range(0, 8):
            peer_bytes_list.append(packed_bytes[i*18: i*18+18])

        peers = []
        for peer_bytes in peer_bytes_list:
            ip_bytes = peer_bytes[0:16]
            port_bytes = peer_bytes[16:18]

            ip = ipaddress.IPv6Address(ip_bytes).compressed
            port = socket.ntohs(hex_to_int(bytes_to_hex(port_bytes)))
            peers.append((ip, port, 0, 0))

        return peers

