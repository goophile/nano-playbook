#!/usr/bin/env python3

import os
import sys

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
            work            = "91B63FDD1754F062",
            hash            = '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948',
            next            = "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
        )

    assert genesis_open_block.calculate_hash().hex().upper() == '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'
    assert genesis_open_block.work_valid()


def test_block_open():
    # 200 bytes of data read from lmdb, it's the first open block (except genesis) in the whole network.
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
            work         = '95EE054972CC823C',
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
    # 144 bytes of data captured from network.
    receive_block_hex = '''
    52430B0B07040003
    0248F7863AF7E9035B7AD7FC0C7F167DEF305D3D8C3EF85197676B0826B794A2
    B55A379FBC452BC50561FD01497296A4F6BF4DF0EF6CDCDCB9DADC9144F0B3EF
    1E5841CB81019BBF8EAE4EFACD9B0AF2162CF30D6BB90BB6574B4EDD973E6C8AE7126D4419568BBED3EB875C4D5E242D9C3BB40E7906FB2AF2F9D5A5D5339F01
    1F256ED32440CCCF
    '''

    network_hex_block = ''.join(receive_block_hex.split()[1:])

    receive_block = Block(
            type       = 'receive',
            previous   = '0248F7863AF7E9035B7AD7FC0C7F167DEF305D3D8C3EF85197676B0826B794A2',
            source     = 'B55A379FBC452BC50561FD01497296A4F6BF4DF0EF6CDCDCB9DADC9144F0B3EF',
            signature  = '1E5841CB81019BBF8EAE4EFACD9B0AF2162CF30D6BB90BB6574B4EDD973E6C8AE7126D4419568BBED3EB875C4D5E242D9C3BB40E7906FB2AF2F9D5A5D5339F01',
            work       = '1F256ED32440CCCF',
            hash       = 'CBAD1775986A8E6C73827F6FF794C5FA17B84067ABB4C2D429EDD75DC5DB2656'
        )

    assert receive_block.calculate_hash().hex().upper() == 'CBAD1775986A8E6C73827F6FF794C5FA17B84067ABB4C2D429EDD75DC5DB2656'
    assert receive_block.work_valid()
    assert receive_block.to_network_bytes().hex().upper() == network_hex_block

    unpacked_block = Block(type='receive')
    unpacked_block.from_network_bytes(network_hex_block)

    assert unpacked_block.calculate_hash().hex().upper() == 'CBAD1775986A8E6C73827F6FF794C5FA17B84067ABB4C2D429EDD75DC5DB2656'


def test_block_change():
    # data read from lmdb, b'change' table.
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
            work            = 'EC39F07202CADC4F',
            hash            = '007CC9DDEC9471235D4E37746052EB518FC321890A67884586DD73B18DABC69B'
        )

    assert change_block.calculate_hash().hex().upper() == '007CC9DDEC9471235D4E37746052EB518FC321890A67884586DD73B18DABC69B'
    assert change_block.work_valid()
    assert change_block.to_storage_bytes().hex().upper() == ''.join(change_block_hex.split())


def test_block_state():
    # 224 bytes of data captured from network.
    state_block_hex = '''
    5243080807030006
    2AC1A3C9A1BF85D0E8C7FC6B62A0D87C40850760FBF9382FF824F6A042FAF61F
    1ED7BB8BBF43DBD9AA5D81E1EDC5F59F95DB714056C0CBE86C9E48AD1C1EF3AE
    3FE80B4BC842E82C1C18ABFEEC47EA989E63953BC82AC411F304D13833D52A56
    000000120D5C7423002A0CDA22000000
    8713D7C032E2E8D6C845FF04EC1F63D9E86EE961A2E61B9D7568EDB79CFE8A9F
    B186EF270BFD779A272D7B52727D06B0990E84D358613B5924464CFD9983559AC9B7DD94912D14405E0BBAB681596CFD37A19E406D2623D73C3148A94699940A
    FCB4E6B3F4DA6EAE
    '''

    network_hex_block = ''.join(state_block_hex.split()[1:])

    # 2AC1A3C9A1BF85D0E8C7FC6B62A0D87C40850760FBF9382FF824F6A042FAF61F == xrb_1cp3nh6t5hw7t5nehz5decifiz41in5p3yzs91qzib9pn33hoxizqo4zos3f
    # 3FE80B4BC842E82C1C18ABFEEC47EA989E63953BC82AC411F304D13833D52A56 == xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1

    state_block = Block(
            type            = 'state',
            account         = 'xrb_1cp3nh6t5hw7t5nehz5decifiz41in5p3yzs91qzib9pn33hoxizqo4zos3f',
            previous        = '1ED7BB8BBF43DBD9AA5D81E1EDC5F59F95DB714056C0CBE86C9E48AD1C1EF3AE',
            representative  = 'xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1',
            balance         = '000000120D5C7423002A0CDA22000000',
            link            = '8713D7C032E2E8D6C845FF04EC1F63D9E86EE961A2E61B9D7568EDB79CFE8A9F',
            signature       = 'B186EF270BFD779A272D7B52727D06B0990E84D358613B5924464CFD9983559AC9B7DD94912D14405E0BBAB681596CFD37A19E406D2623D73C3148A94699940A',
            work            = 'FCB4E6B3F4DA6EAE',
            hash            = 'A5A2E431F88574B2A161C92BD53DAFE05B026902A4C3D9FE33F12234CFFF0D03'
        )

    assert state_block.calculate_hash().hex().upper() == 'A5A2E431F88574B2A161C92BD53DAFE05B026902A4C3D9FE33F12234CFFF0D03'
    assert state_block.work_valid()
    assert state_block.to_network_bytes().hex().upper() == network_hex_block

    unpacked_block = Block(type='state')
    unpacked_block.from_network_bytes(network_hex_block)

    assert unpacked_block.calculate_hash().hex().upper() == 'A5A2E431F88574B2A161C92BD53DAFE05B026902A4C3D9FE33F12234CFFF0D03'


if __name__ == '__main__':
    test_block_state()

