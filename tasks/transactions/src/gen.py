import operator
import random
import os, binascii, hashlib, base58, ecdsa
from math import ceil


def generate_address():
    def ripemd160(x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d

    # generate private key , uncompressed WIF starts with "5"
    priv_key = os.urandom(32)

    # get public key , uncompressed address starts with "1"
    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
    publ_addr_a = b"\x00" + hash160
    checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
    publ_addr_b = base58.b58encode(publ_addr_a + checksum)
    return publ_addr_b.decode()


addrs = [generate_address() for _ in range(100)]
wallets = {addr: 10000 for addr in addrs}
chain = []
for _ in range(3000):
    f, t = random.choice(addrs), random.choice(addrs)
    while wallets[f] == 0:
        f = random.choice(addrs)
    amount = random.randint(1, wallets[f])
    wallets[f] -= amount
    wallets[t] += amount
    miner = random.choice(addrs)
    mined = random.randint(1, ceil(amount / 3))
    wallets[miner] += mined
    chain.append((f, t, amount, miner, mined))

with open("../files/chain.txt", "w") as f:
    print("from,to,amount,miner,mined_amount", file=f)
    for tr in chain:
        print(*tr, sep=',', file=f)
wallets = list(wallets.items())
wallets.sort(key=operator.itemgetter(1))
print(wallets[-1])
