import json

top100 = json.load(open("top100.json"))["EVM"]["Calls"]
top100to1k = json.load(open("top100to1k.json"))["EVM"]["Calls"]
top1kto10k = json.load(open("top1kto10k.json"))["EVM"]["Calls"]
top10kto100k = json.load(open("top10kto100k.json"))["EVM"]["Calls"]

freq100 = json.load(open("freq100.json"))["EVM"]["Calls"]
freq100to1k = json.load(open("freq100to1k.json"))["EVM"]["Calls"]
freq1kto10k = json.load(open("freq1kto10k.json"))["EVM"]["Calls"]
freq10kto100k = json.load(open("freq10kto100k.json"))["EVM"]["Calls"]

freqsenderset100  = set()
freqsenderset100to1k = set()
freqsenderset1kto10k = set()
freqsenderset10kto100k = set()
freqsenderset = set()

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

def find_correlation(top_txns, freq_senders):
    total = 0
    ftd = {}
    for txn in top_txns:
        total += float(txn["sum"])
        if txn["Transaction"]["From"] in freq_senders:
            if txn["Transaction"]["From"] not in ftd:
                ftd[txn["Transaction"]["From"]] = (float(txn["sum"]), 1)
            else:
                ftd[txn["Transaction"]["From"]] = (ftd[txn["Transaction"]["From"]][0]+float(txn["sum"]), ftd[txn["Transaction"]["From"]][1]+1)
        if txn["Transaction"]["To"] in freq_senders:
            if txn["Transaction"]["To"] not in ftd:
                ftd[txn["Transaction"]["To"]] = (float(txn["sum"]), 1)
            else:
                ftd[txn["Transaction"]["To"]] = (ftd[txn["Transaction"]["To"]][0]+float(txn["sum"]), ftd[txn["Transaction"]["To"]][1]+1)
    return (total, len(ftd), ftd)

print("ftd100", find_correlation(top100, freqsenderset100)[:2])
print("ftd100to1k", find_correlation(top100to1k, freqsenderset100to1k)[:2])
print("ftd1kto10k", find_correlation(top1kto10k, freqsenderset1kto10k)[:2])
print("ftd10kto100k", find_correlation(top10kto100k, freqsenderset10kto100k)[:2])
