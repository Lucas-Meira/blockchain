import pytest

from blockchain import BlockChain, Block
from blockchain.core import InvalidBlockException


@pytest.fixture
def blockchain() -> BlockChain:
    return BlockChain()


def test_default_parameters(blockchain: BlockChain):
    assert blockchain._difficulty == 4
    assert blockchain._preffix == '0'


def test_genesis_block_creation(blockchain: BlockChain):
    assert blockchain._last_block.payload.data == "Where it all started"
    assert blockchain._last_block.prev_hash == ''
    assert blockchain._last_block.nonce == 0
    assert blockchain.size == 1


def test_block_creation(blockchain: BlockChain):
    test_data = "New Random Block Data"
    new_block = blockchain.create_block(test_data)

    assert isinstance(new_block, Block)
    assert blockchain.size == 1
    assert new_block.hash == b'0'*256
    assert new_block.nonce == 0

    blockchain.mine(new_block)

    assert new_block.hash != b'0'*256
    assert new_block.nonce != 0

    blockchain.add_block(new_block)
    assert blockchain.size == 2


def test_multiple_block_creation(blockchain: BlockChain):

    for i in range(1, 6):
        test_data = f'Block #{i}'
        new_block = blockchain.create_block(test_data)
        blockchain.mine(new_block)
        blockchain.add_block(new_block)
        assert blockchain.size == i + 1
        assert blockchain._last_block.data == test_data


def test_invalid_block_creation(blockchain: BlockChain):
    test_data = "New Random Block Data"
    new_block = blockchain.create_block(test_data)

    assert isinstance(new_block, Block)
    blockchain.mine(new_block)

    following_prefix = chr(ord(blockchain._preffix) + 1).encode('utf8')

    new_block_hash = new_block.hash
    new_block.header.hash = following_prefix + new_block.hash[1:]

    pytest.raises(InvalidBlockException, blockchain.add_block, block=new_block)

    assert blockchain.size == 1

    new_block.header.hash = new_block_hash

    prev_hash = new_block.prev_hash

    new_block.payload.prev_hash = new_block_hash

    pytest.raises(InvalidBlockException, blockchain.add_block, block=new_block)

    assert blockchain.size == 1

    new_block.payload.prev_hash = prev_hash

    blockchain.add_block(new_block)

    assert blockchain.size == 2
