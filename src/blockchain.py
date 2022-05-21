import json
import time
import typing
from dataclasses import asdict, dataclass

import utils


@dataclass
class Header:
    nonce: int
    hash: bytes


@dataclass
class Payload:
    number: int
    data: str
    timestamp: int
    prev_hash: bytes


@dataclass
class Block:
    header: Header
    payload: Payload

    def __repr__(self) -> str:
        return f"Block<{utils.hexdigest(self.header.hash)[:10]}...>"


class BlockChain:
    def __init__(self, difficulty: int = 4, proof_of_work_preffix: str = '0'):
        self._chain: list[Block] = []

        self._difficulty = difficulty
        self._preffix = proof_of_work_preffix

        self._create_genesis_block()

    @staticmethod
    def _to_json(data: dict[str, str]):
        return json.dumps(data, ensure_ascii=False).encode('utf8')

    def _create_genesis_block(self):
        block_payload = Payload(number=0, data='Where it all started', timestamp=time.time_ns(), prev_hash='')
        block_header = Header(hash=utils.digest(self._to_json(asdict(block_payload))), nonce=0)

        self._chain.append(Block(block_header, block_payload))

    @property
    def _last_block(self) -> Block:
        return self._chain[-1]

    def create_block(self, data: typing.Any) -> Block:
        block_payload = Payload(
            number=self._last_block.payload.number + 1,
            data=json.dumps(data),
            timestamp=time.time_ns(),
            prev_hash=self._last_block.header.hash)

        return Block(Header(0, b'0'*128), block_payload)

    def mine(self, block: Block):
        nonce: int = 0
        start_time = time.time()

        while True:
            payload_dict = asdict(block.payload)
            payload_dict['prev_hash'] = utils.hexdigest(payload_dict['prev_hash'])
            payload_dict['nonce'] = nonce

            hash = utils.digest(self._to_json(payload_dict))

            if not utils.is_hash_proofed(hash, self._difficulty, self._preffix):
                nonce += 1

                continue

            mine_time = time.time() - start_time

            print(f"Took {mine_time:5.5} seconds to mine block #{block.payload.number}!")

            header = Header(nonce, hash)
            block.header = header

            return mine_time

    def _is_new_block_valid(self, block: Block):
        if block.payload.prev_hash != self._last_block.header.hash:
            print(f"Block #{block.payload.number} invalid! Previous hash is {self._last_block.header.hash[:10]!r}, "
                  f"but got {block.header.hash[:10]!r}.")

            return False

        if not utils.is_hash_proofed(block.header.hash, self._difficulty, self._preffix):
            print(f"Block #{block.payload.number} invalid! Its signature is invalid. Got nonce {block.header.nonce}")

            return False

        return True

    def add_block(self, block: Block):
        if self._is_new_block_valid(block):
            self._chain.append(block)

            print(f"Successfully added {block}!")


if __name__ == "__main__":
    blockchain = BlockChain()

    for i in range(100):
        new_block = blockchain.create_block(f"Block #{i}")
        blockchain.mine(new_block)
        blockchain.add_block(new_block)

    print(blockchain._chain)
