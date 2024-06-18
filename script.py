import json

top100 = json.load(open("top100.json"))["EVM"]["Calls"]
top100to1k = json.load(open("top100to1k.json"))["EVM"]["Calls"]
top1kto10k = json.load(open("top1kto10k.json"))["EVM"]["Calls"]
top10kto100k = json.load(open("top10kto100k.json"))["EVM"]["Calls"]

freq100 = json.load(open("freq100.json"))["EVM"]["Calls"]
freq100to1k = json.load(open("freq100to1k.json"))["EVM"]["Calls"]
freq1kto10k = json.load(open("freq1kto10k.json"))["EVM"]["Calls"]
freq10kto100k = json.load(open("freq10kto100k.json"))["EVM"]["Calls"]

freqdep100 = json.load(open("freqdep100.json"))["EVM"]["Calls"]
freqdep100to1k = json.load(open("freqdep100to1k.json"))["EVM"]["Calls"]
freqdep1kto10k = json.load(open("freqdep1kto10k.json"))["EVM"]["Calls"]
freqdep10kto100k = json.load(open("freqdep10kto100k.json"))["EVM"]["Calls"]

freqfull = freq100 + freq100to1k + freq1kto10k + freq10kto100k
freqdepfull = freqdep100 + freqdep100to1k + freqdep1kto10k + freqdep10kto100k

freqsenderset100 = set()
freqsenderset100to1k = set()
freqsenderset1kto10k = set()
freqsenderset10kto100k = set()
freqsenderset = set()

freqdepositorset100 = set()
freqdepositorset100to1k = set()
freqdepositorset1kto10k = set()
freqdepositorset10kto100k = set()
freqdepositorset = set()

for i in freq100:
    freqsenderset100.add(i["Transaction"]["From"])
    freqsenderset.add(i["Transaction"]["From"])
for i in freq100to1k:
    freqsenderset100to1k.add(i["Transaction"]["From"])
    freqsenderset.add(i["Transaction"]["From"])
for i in freq1kto10k:
    freqsenderset1kto10k.add(i["Transaction"]["From"])
    freqsenderset.add(i["Transaction"]["From"])
for i in freq10kto100k:
    freqsenderset10kto100k.add(i["Transaction"]["From"])
    freqsenderset.add(i["Transaction"]["From"])

for i in freqdep100:
    freqdepositorset100.add(i["Transaction"]["From"])
    freqdepositorset.add(i["Transaction"]["From"])
for i in freqdep100to1k:
    freqdepositorset100to1k.add(i["Transaction"]["From"])
    freqdepositorset.add(i["Transaction"]["From"])
for i in freqdep1kto10k:
    freqdepositorset1kto10k.add(i["Transaction"]["From"])
    freqdepositorset.add(i["Transaction"]["From"])
for i in freqdep10kto100k:
    freqdepositorset10kto100k.add(i["Transaction"]["From"])
    freqdepositorset.add(i["Transaction"]["From"])


def find_correlation(top_txns, freq_senders, freq_senders_list):
    total = 0
    ftd = {}
    for txn in top_txns:
        total += float(txn["Transaction"]["ValueInUSD"])
        if txn["Transaction"]["From"] in freq_senders:
            if txn["Transaction"]["From"] not in ftd:
                ftd[txn["Transaction"]["From"]] = (
                    float(txn["Transaction"]["ValueInUSD"]),
                    1,
                )
            else:
                ftd[txn["Transaction"]["From"]] = (
                    ftd[txn["Transaction"]["From"]][0]
                    + float(txn["Transaction"]["ValueInUSD"]),
                    ftd[txn["Transaction"]["From"]][1] + 1,
                )
        if txn["Transaction"]["To"] in freq_senders:
            if txn["Transaction"]["To"] not in ftd:
                ftd[txn["Transaction"]["To"]] = (
                    float(txn["Transaction"]["ValueInUSD"]),
                    1,
                )
            else:
                ftd[txn["Transaction"]["To"]] = (
                    ftd[txn["Transaction"]["To"]][0]
                    + float(txn["Transaction"]["ValueInUSD"]),
                    ftd[txn["Transaction"]["To"]][1] + 1,
                )
    ftotal = 0
    ftxn_count = 0
    for sender in freq_senders_list:
        ftotal += float(sender["Transaction"]["ValueInUSD"])
        ftxn_count += float(sender["tx_count"])
    return (
        total,
        ftotal,
        ftxn_count,
        len(ftd),
        len(top_txns),
        100 * len(ftd) / len(top_txns),
        ftd,
    )


print("ftd100", find_correlation(top100, freqsenderset100, freq100)[:6])
print("ftd100to1k", find_correlation(top100to1k, freqsenderset100to1k, freq100to1k)[:6])
print("ftd1kto10k", find_correlation(top1kto10k, freqsenderset1kto10k, freq1kto10k)[:6])
print(
    "ftd10kto100k",
    find_correlation(top10kto100k, freqsenderset10kto100k, freq10kto100k)[:6],
)
print("ftd100full", find_correlation(top100, freqsenderset, freqfull)[:6])
print("ftd100to1kfull", find_correlation(top100to1k, freqsenderset, freqfull)[:6])
print("ftd1kto10kfull", find_correlation(top1kto10k, freqsenderset, freqfull)[:6])
print(
    "ftd10kto100kfull",
    find_correlation(top10kto100k, freqsenderset, freqfull)[:6],
)

print("fts100", find_correlation(top100, freqdepositorset100, freqdep100)[:6])
print(
    "fts100to1k",
    find_correlation(top100to1k, freqdepositorset100to1k, freqdep100to1k)[:6],
)
print(
    "fts1kto10k",
    find_correlation(top1kto10k, freqdepositorset1kto10k, freqdep1kto10k)[:6],
)
print(
    "fts10kto100k",
    find_correlation(top10kto100k, freqdepositorset10kto100k, freqdep10kto100k)[:6],
)
print("fts100", find_correlation(top100, freqdepositorset, freqdepfull)[:6])
print("fts100to1k", find_correlation(top100to1k, freqdepositorset, freqdepfull)[:6])
print("fts1kto10k", find_correlation(top1kto10k, freqdepositorset, freqdepfull)[:6])
print(
    "fts10kto100k",
    find_correlation(top10kto100k, freqdepositorset, freqdepfull)[:6],
)
