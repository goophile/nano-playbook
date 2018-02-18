#!/usr/bin/env python3

import os
import sys
import pytest

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from libs.block import Block


def test_genesis_block_open():
    # 200 bytes of data read from lmdb, it's the first block in the whole network.
    genesis_open_block_hex = '''
    E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA
    E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA
    E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA
    9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02
    91B63FDD1754F062
    A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293
    '''

    # the hex string can be cut into pieces and fit into a Block
    # 'xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3' == 'E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA'

    genesis_open_block = Block(
            type            = "open",
            source          = "E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA",
            representative  = "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
            account         = "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
            signature       = "9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02",
            work            = "91b63fdd1754f062",
            hash            = '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948',
            next            = "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
        )

    assert genesis_open_block.calculate_hash().hex().upper() == '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'
    assert genesis_open_block.work_valid()


def test_block_open():
    landing_open_block_hex = '''
    A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293
    2399A083C600AA0572F5E36247D978FCFC840405F8D4B6D33161C0066A55F431
    059F68AAB29DE0D3A27443625C7EA9CDDB6517A8B76FE37727EF6A4D76832AD5
    E950FFDF0C9C4DAF43C27AE3993378E4D8AD6FA591C24497C53E07A3BC80468539B0A467992A916F0DDA6F267AD764A3C1A5BDBD8F489DFAE8175EEE0E337402
    B1A152A497C097E9
    18563C814A54535B7C12BF76A0E23291BA3769536634AB90AD0305776A533E8E
    '''

    # xrb_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy == 2399A083C600AA0572F5E36247D978FCFC840405F8D4B6D33161C0066A55F431
    # xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo == 059F68AAB29DE0D3A27443625C7EA9CDDB6517A8B76FE37727EF6A4D76832AD5

    landing_open_block = Block(
            type            = "open",
            source          = "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
            representative  = "xrb_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy",
            account         = "xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo",
            signature       = "E950FFDF0C9C4DAF43C27AE3993378E4D8AD6FA591C24497C53E07A3BC80468539B0A467992A916F0DDA6F267AD764A3C1A5BDBD8F489DFAE8175EEE0E337402",
            work            = "B1A152A497C097E9",
            hash            = '90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35',
            next            = "18563C814A54535B7C12BF76A0E23291BA3769536634AB90AD0305776A533E8E"
        )

    assert landing_open_block.calculate_hash().hex().upper() == '90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35'
    assert landing_open_block.work_valid()
    assert landing_open_block.to_storage_bytes().hex().upper() == ''.join(landing_open_block_hex.split())


def test_block_send():
    # 184 bytes of data read from lmdb, the first send block of the genesis account.
    genesis_send_block_hex = '''
    991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948
    059F68AAB29DE0D3A27443625C7EA9CDDB6517A8B76FE37727EF6A4D76832AD5
    FD89D89D89D89D89D89D89D89D89D89D
    5B11B17DB9C8FE0CC58CAC6A6EECEF9CB122DA8A81C6D3DB1B5EE3AB065AA8F8CB1D6765C8EB91B58530C5FF5987AD95E6D34BB57F44257E20795EE412E61600
    95EE054972CC823C
    28129ABCAB003AB246BA22702E0C218794DFFF72AD35FD56880D8E605C0798F6
    '''

    storage_hex_raw = ''.join(genesis_send_block_hex.split())

    # 'xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo' == '059F68AAB29DE0D3A27443625C7EA9CDDB6517A8B76FE37727EF6A4D76832AD5'

    genesis_send_block = Block(
            type         = 'send',
            previous     = '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948',
            destination  = 'xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo',
            balance      = 'FD89D89D89D89D89D89D89D89D89D89D',
            signature    = '5B11B17DB9C8FE0CC58CAC6A6EECEF9CB122DA8A81C6D3DB1B5EE3AB065AA8F8CB1D6765C8EB91B58530C5FF5987AD95E6D34BB57F44257E20795EE412E61600',
            work         = '95ee054972cc823c',
            hash         = 'A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293',
            next         = '28129ABCAB003AB246BA22702E0C218794DFFF72AD35FD56880D8E605C0798F6'
        )

    assert genesis_send_block.calculate_hash().hex().upper() == 'A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293'
    assert genesis_send_block.work_valid()
    assert genesis_send_block.to_storage_bytes().hex().upper() == storage_hex_raw

    unpacked_block = Block(type='send')
    unpacked_block.from_storage_bytes(storage_hex_raw)

    assert unpacked_block.calculate_hash().hex().upper() == 'A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293'


def test_block_receive():
    # 144 bytes of data captured from network
    receive_block_hex = '''
    5243050501030003
    6B6181C1AC75DAABD30CEAE15D44D30D238198968A5A794E057DC36503120550
    7716EF323E3079CF8BF9E7EFD1C40F60F8DD3251F24D3F455098EEA90A33572E
    3226710D0BD7D3E355F3F1D985AF8BA1B2EB9B346752DEF6F8C14C2C0E91C663A34B3F800E332E48913F7F1F65FF86342490B9C2F97D4FFF50B8F98ACD3DC90F
    86C3565BE806C52B
    '''

    network_hex_raw = ''.join(receive_block_hex.split()[1:])

    receive_block = Block(
            type       = 'receive',
            previous   = '6b6181c1ac75daabd30ceae15d44d30d238198968a5a794e057dc36503120550',
            source     = '7716ef323e3079cf8bf9e7efd1c40f60f8dd3251f24d3f455098eea90a33572e',
            signature  = '3226710d0bd7d3e355f3f1d985af8ba1b2eb9b346752def6f8c14c2c0e91c663a34b3f800e332e48913f7f1f65ff86342490b9c2f97d4fff50b8f98acd3dc90f',
            work       = '86c3565be806c52b',
            hash       = '7C2163FE063C9195E4C151646F6819E568F55BD1392182E50410D347336BCDF0'
        )

    assert receive_block.calculate_hash().hex().upper() == '7C2163FE063C9195E4C151646F6819E568F55BD1392182E50410D347336BCDF0'
    assert receive_block.work_valid()
    assert receive_block.to_network_bytes().hex().upper() == network_hex_raw

    unpacked_block = Block(type='receive')
    unpacked_block.from_network_bytes(network_hex_raw)

    assert unpacked_block.calculate_hash().hex().upper() == '7C2163FE063C9195E4C151646F6819E568F55BD1392182E50410D347336BCDF0'


def test_block_change():
    # data read from lmdb, b'change' table
    change_block_hex = '''
    D228A12E8E10183AFB0CB9C444C88B0E6FB6F03572B41F3C3DB447E7459BC038
    023185665A78C297F803FE361C7818F6B9D5EB274E9DFCD2ACE1F92C6A9AF13D
    F25DED3FC35937CFFBC4150FCFC81D27B80966ED6D9C3E42EF10278A4264436F7B935744748BAC4A73952585B9C0A0B788019EFB6F3E52D8CB8AEF30DACCD300
    EC39F07202CADC4F
    0000000000000000000000000000000000000000000000000000000000000000
    '''

    # 023185665A78C297F803FE361C7818F6B9D5EB274E9DFCD2ACE1F92C6A9AF13D == xrb_11jjiom7ny84kzw19zjp5jw3jxostqokgmnxzmbcsrhs7jobowbxr19dwbyt

    change_block = Block(
            type            = 'change',
            previous        = 'D228A12E8E10183AFB0CB9C444C88B0E6FB6F03572B41F3C3DB447E7459BC038',
            representative  = 'xrb_11jjiom7ny84kzw19zjp5jw3jxostqokgmnxzmbcsrhs7jobowbxr19dwbyt',
            signature       = 'F25DED3FC35937CFFBC4150FCFC81D27B80966ED6D9C3E42EF10278A4264436F7B935744748BAC4A73952585B9C0A0B788019EFB6F3E52D8CB8AEF30DACCD300',
            work            = 'ec39f07202cadc4f',
            hash            = '007CC9DDEC9471235D4E37746052EB518FC321890A67884586DD73B18DABC69B'
        )

    assert change_block.calculate_hash().hex().upper() == '007CC9DDEC9471235D4E37746052EB518FC321890A67884586DD73B18DABC69B'
    assert change_block.work_valid()
    assert change_block.to_storage_bytes().hex().upper() == ''.join(change_block_hex.split())

