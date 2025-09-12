import requests
from utility import toBinary
from utilityTransazioni import getCoinbase
from tqdm import tqdm
from utility import decode_hex_to_text

def estraiMessaggiMiner(lista_blocchi):
    """
    Estrae i messaggi dei miner dai blocchi passati.
    
    Per ogni blocco:
    - Legge il campo vin[0]["coinbase"] (messaggio principale)
    - Estrae eventuali OP_RETURN negli output della coinbase
    
    Ritorna una lista di dizionari con:
        - block_id: ID del blocco
        - version_bin: versione del blocco in binario
        - coinbase_msg: messaggio principale del miner
        - op_returns: lista di OP_RETURN della coinbase
    """
    risultati = []

    # Barra di progresso globale
    for block in tqdm(lista_blocchi, desc="Analizzando blocchi", unit="blocco"):
        block_id = block["id"]
        version_bin = toBinary(block["version"])
        coinbase_tx = getCoinbase(block_id)

        # Decodifica messaggio principale della coinbase
        coinbase_msg = decode_hex_to_text(coinbase_tx["vin"][0]["coinbase"])

        # Estrai e decodifica eventuali OP_RETURN della coinbase
        op_returns = []
        for vout in coinbase_tx["vout"]:
            if vout["scriptpubkey_type"] == "nulldata":
                op_returns.append(decode_hex_to_text(vout["scriptpubkey"]))

        risultati.append({
            "block_id": block_id,
            "version_bin": version_bin,
            "coinbase_msg": coinbase_msg,
            "op_returns": op_returns
        })

    return risultati

# Funzione che stampa i messaggi dei miner dai risultati di estraiMessaggiMiner
def stampaMessaggiMiner(risultati):
    for i in range(len(risultati)):
        risultato = risultati[i]
        print("Blocco: " + risultato['block_id'])
        print("Version(bin): " + risultato['version_bin'])
        print("  Coinbase OP_RETURN outputs:")
        if risultato["op_returns"]:
            for j in range(len(risultato["op_returns"])):
                output = risultato["op_returns"][j]
                print("    Output " + str(j) + ": " + output)
        else:
            print("    Nessun output OP_RETURN trovato")
        print("-" * 50)

# Funzione che stampa i messaggi dei miner e li salva su file
def stampaMessaggiMinerSuFile(risultati, filename="messaggi_miner.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(len(risultati)):
            risultato = risultati[i]
            f.write("Blocco: " + risultato['block_id'] + "\n")
            f.write("Version(bin): " + risultato['version_bin'] + "\n")
            f.write("  Coinbase OP_RETURN outputs:\n")
            
            if risultato["op_returns"]:
                for j in range(len(risultato["op_returns"])):
                    output = risultato["op_returns"][j]
                    f.write("    Messaggio " + str(j) + ": " + output + "\n")
            else:
                f.write("    Nessun output OP_RETURN trovato\n")
            
            f.write("-" * 50 + "\n")

    print("Dati salvati su", filename)
