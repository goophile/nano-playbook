Raiblocks Account
=================


# ED25519

First, please read through the white paper, [RaiBlocks: A Feeless Distributed Cryptocurrency Network](https://raiblocks.net/media/RaiBlocks_Whitepaper__English.pdf).

Then, please also read this article, [How do Ed5519 keys work?](https://blog.mozilla.org/warner/2011/11/29/ed25519-keys/).

As the white paper says, "RaiBlocks uses a modified ED25519 elliptic curve algorithm with Blake2b hashing for all digital signatures". So when we do the signing work, we should also modify the algorithm.

Here we use [python-pure25519](https://github.com/warner/python-pure25519). Clone the code and edit `pure25519/eddsa.py`, change SHA512 to blake2b(64).

```py
def H(m):
    return hashlib.sha512(m).digest()
```

```py
from pyblake2 import blake2b
def H(m):
    return blake2b(m).digest()
```


# From RaiBlocks seed to ED25519 keys

The term `seed` may have two meanings, the `RaiBlocks seed` or the `ED25519 seed`.

Both seeds should be kept in secret and never sent to others.

The Raiblocks seed is the string you get when clicking `Backup wallet seed` in the wallet. It's a 64-characters hex string, and contains 32 bytes of binary data. It's randomly generated when you first open your wallet software. You can also generate it with some other random number generator.

The ED25519 seed is generated from the RaiBlocks seed. In the ed25519 workflow, different implementations may use different parts as the private key. To avoid confusion, let's use the terms `ed25519 seed`, `signing key`, and `private key` to refer the same thing. And `verifying key` and `public key` are also the same thing.

To generate the signing key, the RaiBlocks seed concatenated with a 4-bytes index is hashed with blake2b.

Please note that, after concatenating with zero-valued binary data, the hash of a string will change, and the number of zeros also matters.

```py
>>> blake2b(bytes.fromhex('aaaa'), digest_size=32).hexdigest()
'f17acd16494a31a141c89aac7d9027a145fabb86bcc28c848541d1061a6e64a0'
>>> blake2b(bytes.fromhex('aaaa0000'), digest_size=32).hexdigest()
'41db0f324a2bb8ec337cd82aab7dbfad41dc3971efa270efa27a365e69c31f3d'
```

The Raiblocks seed, the signing key, and the verifying key, they are all 32 bytes long. After converted to hex string, they are all 64 characters long.


# Address format

The RaiBlocks address is in fact a base32 encoded string of the verifying key.

To encode binary data into base32, the data bits length must be multiples of 5. The verifying key is 32 bytes, or 256 bits long, so 4 bits must be added. In RaiBlocks, 4 bits of zeros are inserted into the beginning. So the total length is 260 bits, and the first 5 bits must be `00000` or `00001`. After encoding, there are 52 characters.

According to Colin LeMahieu's note([Version 7.3.0 Released](https://groups.google.com/forum/#!topic/raiblocks/RynIszapBvk)), the base32 chosen is z-base-32 like. In RaiBlocks, the alphabet is "13456789abcdefghijkmnopqrstuwxyz". The base32 encoded string is then added to a prefix "xrb_". And since the first base32 5-bits data must be 0 or 1, the address must be started with "xrb_1" or "xrb_3".

There is also a checksum mechanism in the address. The verifying key is hashed to 5-bytes data with blake2b, and then the data is reversed byte by byte. The reversed data is also encoded to base32, producing a 8-characters string.

The prefix "xrb_", concatenated with the base32 encoded verifying key, and the base32 encoded checksum, has a total length of 64 characters. That is the RaiBlocks address.

To get the verifying key, we can slice up the address, and decode the key part with base32 alphabet and remove the heading 4-bits zeros.

