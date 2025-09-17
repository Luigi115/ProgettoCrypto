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

 #Decodifica gli opreturn e li impacchetta in JSON
def estraiOpReturnJSON(tx):
    risultati = {}
    op_returns = estraiOpReturn(tx)
    
    for i, vout in enumerate(op_returns):
        # decodifica lo scriptpubkey in testo leggibile
        msg = decode_hex_to_text(vout.get("scriptpubkey", ""))
        risultati[f"output {i}"] = msg
    
    return risultati