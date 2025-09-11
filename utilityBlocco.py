import requests
from utility import toBinary

URL = "https://mempool.space/api"

#Ritorna gli ultimi 'n' blocchi dalla rete(la API è programmata in modo llimitato)
def listaBlocchi(n):
    url = URL + "/blocks"
    response = requests.get(url)
    response.raise_for_status()
    blocks = response.json()
    return blocks[:n] 

#Ritorna la lista di tutti i blocchi
def listaBlocchiTotale():
    blocchi = []
    
    # Prendi l'ultimo blocco
    lastBlocco = ultimoBlocco()  # qui chiamiamo la funzione
    blocchi.append(lastBlocco)
    
    # qui prendiamo l'id dell'ultimo blocco
    idBlocco = lastBlocco["id"]

    # Cicla indietro fino al blocco genesis
    while True:
        url_blocco = URL + "/block/" + idBlocco
        response = requests.get(url_blocco)
        response.raise_for_status()
        block = response.json()

        # Se c'è un blocco precedente, aggiorna idBlocco e aggiungi il blocco
        if "previousblockhash" in block:
            idBlocco = block["previousblockhash"]
            url_prev = URL + "/block/" + idBlocco
            response = requests.get(url_prev)
            response.raise_for_status()
            bloccoPrecedente = response.json()
            blocchi.append(bloccoPrecedente)
        else:
            break  # siamo arrivati al blocco genesis

    return blocchi

# Ritorna gli ultimi 'n' blocchi
def listaUltimiNBlocchi(n):
    blocchi = []
    
    # Prendi l'ultimo blocco
    lastBlocco = ultimoBlocco()
    blocchi.append(lastBlocco)
    
    # Prendi l'id dell'ultimo blocco
    idBlocco = lastBlocco["id"]

    # Cicla indietro fino al blocco genesis o fino a n blocchi
    while len(blocchi) < n:
        url_blocco = URL + "/block/" + idBlocco
        response = requests.get(url_blocco)
        response.raise_for_status()
        block = response.json()

        if "previousblockhash" in block:
            idBlocco = block["previousblockhash"]
            url_prev = URL + "/block/" + idBlocco
            response = requests.get(url_prev)
            response.raise_for_status()
            bloccoPrecedente = response.json()
            blocchi.append(bloccoPrecedente)
        else:
            break  # siamo arrivati al blocco genesis

    return blocchi



# Stampa tutti i blocchi di una lista
def stampaListaBlocchi(blocks):
    for block in blocks:
        stampaBlocco(block)


#utility blocco singolo
#Ritorna l'ultimo blocco minato
def ultimoBlocco():
    url = URL + "/blocks"
    response = requests.get(url)
    response.raise_for_status()
    blocks = response.json()
    return blocks[0]

#Stampa del blocco in modo più leggibile 
def stampaBlocco(block):
    print("Blocco:")
    print("  Numero del blocco:", block["height"])
    print("  Id:", block["id"])
    print("  Timestamp:", block["timestamp"])
    print("  Numero tx:", block["tx_count"])
    print("  Miner:", block.get("extras", {}).get("pool", "N/A"))
    
#Stampa l'header del blocco
def stampaHeader(block):
    print("Header del blocco:")
    print("  Versione:", block.get("version"))
    print("  Versione(binario):", toBinary(block.get("version")))
    print("  Previous Block Hash:", block.get("previousblockhash"))
    print("  Merkle Root:", block.get("merkle_root"))
    print("  Timestamp:", block.get("timestamp"))
    print("  Bits (difficoltà):", block.get("bits"))
    print("  Nonce:", block.get("nonce"))
    print("-" * 50)
