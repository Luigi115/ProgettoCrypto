import requests
from utility import toBinary


def estraiMessaggiMiner(lista_blocchi):
    risultati = []
    for block in lista_blocchi:
        block_id = block["id"]
        version_bin = toBinary(block["version"])
        coinbase_tx = getCoinbase(block_id)

        # estrai tutti gli OP_RETURN
        op_returns = []
        for vout in coinbase_tx["vout"]:
            if vout["scriptpubkey_type"] == "nulldata":
                op_returns.append(vout["scriptpubkey"])

        risultati.append({
            "block_id": block_id,
            "version_bin": version_bin,
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
