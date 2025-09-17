import requests

URL = "https://mempool.space/api"

#Ritorna la lista di transazioni di un blocco
def getTransazioni(block_hash):
    url = URL + "/block/" + block_hash + "/txs"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

#Ritorna la coinbase transaction di un blocco: la prima transazione
def getCoinbase(block_hash):
    txs = getTransazioni(block_hash)
    coinbase_tx = txs[0]  # prima transazione
    return coinbase_tx

# Ritorna le coinbase transaction di una lista di blocchi, includendo id e numero del blocco
def getCoinbaseDaBlocchi(lista_blocchi):
    coinbase_txs = []
    for block in lista_blocchi:
        coinbase_tx = getCoinbase(block["id"])  # ottieni la coinbase
        # Aggiungi info sul blocco
        coinbase_tx["block_id"] = block["id"]
        coinbase_tx["block_height"] = block.get("height", None)
        coinbase_txs.append(coinbase_tx)
    return coinbase_txs



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


