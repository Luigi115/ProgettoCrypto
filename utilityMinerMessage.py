from tqdm import tqdm
from utility import toBinary, decode_hex_to_text
from utilityTransazioni import getCoinbase

#Estrae tutti gli output OP_RETURN da una transazione.
def estraiOpReturn(tx):
    op_returns = []
    for vout in tx.get("vout", []):
        # Controlla se l'output è OP_RETURN
        if vout.get("scriptpubkey_type", "").lower() == "op_return":
            op_returns.append(vout)
    return op_returns

# Estrae tutti gli output OP_RETURN da una lista di transazioni, includendo info sul blocco
def estraiOpReturnDaTransazioni(transazioni):
    risultati = []

    for tx in transazioni:
        txid = tx.get("txid", "")
        block_id = tx.get("block_id", "")
        block_height = tx.get("block_height", "")
        op_returns = []

        for vout in tx.get("vout", []):
            if vout.get("scriptpubkey_type", "").lower() == "op_return":
                # prendiamo solo scriptpubkey_asm
                op_returns.append(vout.get("scriptpubkey_asm", ""))

        risultati.append({
            "txid": txid,
            "block_id": block_id,
            "block_height": block_height,
            "op_return": op_returns
        })

    return risultati

# Restituisce solo il block_height e la lista degli OP_RETURN di ogni blocco.
def filtraOpReturnPerBlocco(lista_blocchi):
    risultati = []

    for blocco in lista_blocchi:
        blocco_filtrato = {
            "block_height": blocco.get("block_height"),
            "op_return": blocco.get("op_return", [])
        }
        risultati.append(blocco_filtrato)

    return risultati

#
def stampaOpReturnPerBlocco(lista_blocchi):
    for blocco in lista_blocchi:
        print(f"Blocco numero: {blocco.get('block_height')}")
        print("-" * 50)
        op_return_list = blocco.get("op_return", [])
        for idx, op in enumerate(op_return_list, 1):
            print(f"{idx}. {op}")
        print("\n")  # Riga vuota tra i blocchi

 #Decodifica gli opreturn e li impacchetta in JSON
def estraiOpReturnJSON(tx):
    risultati = {}
    op_returns = estraiOpReturn(tx)
    
    for i, vout in enumerate(op_returns):
        # decodifica lo scriptpubkey in testo leggibile
        msg = decode_hex_to_text(vout.get("scriptpubkey", ""))
        risultati[f"output {i}"] = msg
    
    return risultati

