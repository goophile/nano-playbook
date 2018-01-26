#!/usr/bin/env python3


from libs.block import Block
from libs.account import Account


open_blk = Block(
        type            = 'open',
        account         = 'xrb_15p3efm6ukq85dg6b7ptcpdbqraeobys1q7s5sqtmxd5zhbnz46f6i1rn7ye',
        source          = '61952D991F71B6D74A455FAADC8DBEE7EEF1C5BE35A23A74B77A3FF6D0BE1DCE',
        representative  = 'xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4',
        hash            = '763F0A5435D8C931DB5420F64E105B9712C4EDA48DE8301B7354EE84BA8BEB42',
        signature       = '52F076EDB530FEBA42A51016AB730705F824B685E7ED57D6D13FD4F9779D1310EF90D5BFFD1A2D5F40B47C9D1DA8FE408C0C993E445B1E71335BB039C0F4C40E',
        work            = 'bbf3f1cab035d645'
    )

send_blk = Block(
        type         = 'send',
        previous     = '221AF5CCED1667E2B030126E684BF1FDE38355611FB7B7698645EC01333B9C91',
        destination  = 'xrb_1prtz1bfwt1xzxunxtriwfxbtuxb6o7nrg6m3zzn77eyntx64bd1z6anpugu',
        balance      = '02F246DC298E25C40B68142878000000',
        hash         = 'CF0427E92F6E9AE33B943C42C24AF823A180DC8EA27C01F3DB2DFE2FF3D7BD23',
        signature    = '9C2F0A6F1BA18BA344DB44E8EFA660F22C6C674D4C766273569B177BEACDA7448C3CA03A74382F32899713544ABAD374D1C135DDA430DAEB973AAC3DC7A28408',
        work         = '0ce26092a9781e9c'
    )

receive_blk = Block(
        type       = 'receive',
        previous   = '763F0A5435D8C931DB5420F64E105B9712C4EDA48DE8301B7354EE84BA8BEB42',
        source     = 'E0284907FE2867BB7F6B0BCEB197F999FBDCC4C528065A07CCC36C0C0B3F7D38',
        hash       = '22C276C1EE449AF9F80DEB2AC226540B61C8F591D8BB160D5E2FFD0348E8E44D',
        signature  = '65015F22631E3AC14B8226FE530111547E1D14CCB53C4DABD6F8923248171202347E6A841C3726C57A6161762DD5FF359C89DAA6F4AFBF8281542F2BFFC64E07',
        work       = '447792ae2311500c'
    )

change_blk = Block(
        type            = 'change',
        previous        = '',
        representative  = 'xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4',
        hash            = '',
        signature       = '',
        work            = ''
    )


print(open_blk.calculate_hash().hex().upper())
print(send_blk.calculate_hash().hex().upper())
print(receive_blk.calculate_hash().hex().upper())

open_account = Account(address=open_blk.account)
print(open_account.signature_valid(open_blk.hash, open_blk.signature))

print(open_blk.work_valid())
print(send_blk.work_valid())
print(receive_blk.work_valid())

print(open_blk.generate_work().hex())
