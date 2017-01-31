import os
from jsonrpc_requests import Server

server = Server('http://btcrpc:btc@ram5.bo:8332')

def get_cb(tx_id):
    print 'bcl decoderawtransaction `bcl getrawtransaction %s`' % tx_id
    tx = server.decoderawtransaction(server.getrawtransaction(tx_id))
    try:
        address = tx['vout'][0]['scriptPubKey']['addresses'][0]
    except:
        address = None
    return tx['vin'][0]['coinbase'], tx['vout'][0]['value'], address


def get_block(block_hash):
    block = server.getblock(block_hash)
    return block_hash, block['previousblockhash'], block['time'], block['bits'], block['tx'][0]


def get_last_hash():
    if not os.path.exists('last_hash'):
        return None
    with file('last_hash', 'r') as f:
        return f.read()


def set_last_hash(block_hash):
    with file('last_hash', 'w') as f:
        return f.write(block_hash)


def save_block(*data):
    with file('blocks', 'a') as f:
        f.write(' '.join(map(str, data)))
        f.write('\n')


next_block_hash = get_last_hash() or server.getbestblockhash()

i = 0
while True:
    i += 1
    block_hash, next_block_hash, time, bits, coinbase_id = get_block(next_block_hash)
    coinbase, value, address = get_cb(coinbase_id)
    save_block(block_hash, time, bits, coinbase, value, address)
    print i, block_hash, time, bits, coinbase, value, address

    if i % 100 == 0:
        set_last_hash(next_block_hash)
