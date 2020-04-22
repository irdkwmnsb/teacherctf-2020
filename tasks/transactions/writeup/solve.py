import operator

with open("chain.txt") as f:
    tr = f.readlines()[1:]

wallet = {}
for line in tr:
    f, t, amount, miner, mined_amount = line.split(",")
    amount = int(amount)
    mined_amount = int(mined_amount)
    wallet[f] = wallet.get(f, 10000) - amount
    wallet[t] = wallet.get(t, 10000) + amount
    wallet[miner] = wallet.get(miner, 10000) + mined_amount

wallet = list(wallet.items())
wallet.sort(key=operator.itemgetter(1))
print(wallet[-1])