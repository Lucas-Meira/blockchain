import pytest

import blockchain.utils as utils
from hashlib import sha256


def test_hexdigest_valid_entry():
    entry = b'One Test Message'

    assert utils.hexdigest(entry) == sha256(entry).hexdigest()


def test_hexdigest_invalid_entry():
    entry = 'One Test Message'

    with pytest.raises(TypeError):
        utils.hexdigest(entry)


def test_digest_valid_entry():
    entry = b'One Test Message'

    assert utils.digest(entry) == sha256(entry).digest()


def test_digest_invalid_entry():
    entry = 'One Test Message'

    with pytest.raises(TypeError):
        utils.digest(entry)


def test_proofed_hash():
    proofed_hash = bytes.fromhex('00009bf721b1d923f01236d7d3ae0ade1c04fe22fa02f6e5308b757e37631ecc')

    assert utils.is_hash_proofed(proofed_hash, 4, '0') == True

    proofed_hash = bytes.fromhex('000009bf721b1d923f01236d7d3ae0ade1c04fe22fa02f6e5308b757e37631ec')

    assert utils.is_hash_proofed(proofed_hash, 4, '0') == True

    proofed_hash = bytes.fromhex('00000000001b1d923f01236d7d3ae0ade1c04fe22fa02f6e5308b757e37631ec')

    assert utils.is_hash_proofed(proofed_hash, 10, '0') == True

    proofed_hash = bytes.fromhex('55549bf721b1d923f01236d7d3ae0ade1c04fe22fa02f6e5308b757e37631ecc')

    assert utils.is_hash_proofed(proofed_hash, 3, '5') == True


def test_unproofed_hash():
    unproofed_hash = bytes.fromhex('00019bf721b1d923f01236d7d3ae0ade1c04fe22fa02f6e5308b757e37631ecc')

    assert utils.is_hash_proofed(unproofed_hash, 4, '0') == False

    unproofed_hash = bytes.fromhex('00129bf721b1d923f01236d7d3ae0ade1c04fe22fa02f6e5308b757e37631ecc')

    assert utils.is_hash_proofed(unproofed_hash, 4, '0') == False
