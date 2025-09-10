import requests
from utility import toBinary

URL = "https://mempool.space/api"

#Ritorna la lista di transazioni di un blocco
def getTransazioni(block_hash):
    url = URL + "/block/" + block_hash + "/txs"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

#Ritorna la coinbase transaction: la prima transazione
def getCoinbase(block_hash):
    txs = getTransazioni(block_hash)
    coinbase_tx = txs[0]  # prima transazione
    return coinbase_tx


# Stampa tutte le transazioni di un blocco in modo leggibile
def stampaTransazioni(txs):
    for idx, tx in enumerate(txs):
        print(f"Transazione {idx+1}/{len(txs)}:")
        print("  txid:", tx["txid"])
        print("  Numero input:", len(tx["vin"]))
        print("  Numero output:", len(tx["vout"]))

        # Output
        print("  Output:")
        for i, vout in enumerate(tx["vout"]):
            script_type = vout["scriptpubkey_type"]
            value = vout["value"] / 1e8  # convertiamo da satoshi a BTC
            if script_type == "nulldata":
                print("    Output", i, "- OP_RETURN:", vout["scriptpubkey"])
            else:
                print("    Output", i, "-", script_type, ":", value, "BTC")
        
        print("-" * 50)  # separatore tra le transazioni

#Ritorna i dettagli completi di una transazione (JSON)
def dettagliTransazione(txid):
    url = URL + "/tx/" + txid
    response = requests.get(url)
    response.raise_for_status()
    return response.json()