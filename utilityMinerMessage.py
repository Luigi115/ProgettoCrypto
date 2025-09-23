from tqdm import tqdm
from utility import toBinary, decode_hex_to_text, filtra_ascii
from utilityTransazioni import getCoinbase
import string

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

#stampa gli opreturn per bene sullo schermo
def stampaOpReturnPerBlocco(lista_blocchi):
    for blocco in lista_blocchi:
        print(f"Blocco numero: {blocco.get('block_height')}")
        print("-" * 50)
        op_return_list = blocco.get("op_return", [])
        for idx, op in enumerate(op_return_list, 1):
            print(f"{idx}. {op}")
        print("\n")  # Riga vuota tra i blocchi
        
        
        
#raccoglie i messaggi degli op_return, toglie "!"
def collect_op_return_messages(blocks):
    """
    Raccoglie i messaggi OP_RETURN dai blocchi, filtra quelli che iniziano con '!'
    Restituisce un dizionario: {block_height: [messaggi]}
    """
    result = {}
    for block in blocks:
        height = block.get("block_height", "N/A")
        messages = []
        for msg in block.get("op_return", []):
            hex_data = msg.split()[-1]
            decoded = filtra_ascii(decode_hex_to_text(hex_data)).strip()
            if decoded and not decoded.startswith("!"):
                messages.append(decoded)
        if messages:
            result[height] = messages
    return result

def print_op_return_messages(messages_dict):
    """
    Stampa i messaggi raccolti in modo ordinato per block height
    """
    for height, messages in messages_dict.items():
        print(f"block height: {height}")
        for i, msg in enumerate(messages, start=1):
            print(f"  messaggio {i}: {msg}")
        print("\n")


#categorizzi i messaggi degli opreturn        
def categorize_messages(messages_dict):
    """
    Catalogo i messaggi in 4 categorie: CORE, RSKBLOCK, EXSAT, sys.
    Ogni categoria conterrà una lista di dizionari:
    {"block_height": ..., "messaggio_n": ..., "contenuto": ...}
    """
    categories = {
        "CORE": [],
        "RSKBLOCK": [],
        "EXSAT": [],
        "sys": []
    }

    for height, messages in messages_dict.items():
        for i, msg in enumerate(messages, start=1):
            entry = {
                "block_height": height,
                "messaggio_n": i,
                "contenuto": msg
            }

            if msg.startswith("CORE"):
                categories["CORE"].append(entry)
            elif msg.startswith("RSKBLOCK"):
                categories["RSKBLOCK"].append(entry)
            elif msg.startswith("EXSAT"):
                categories["EXSAT"].append(entry)
            elif msg.startswith("sys"):
                categories["sys"].append(entry)

    return categories


def print_categorized_messages(categorized):
    """
    Stampa i messaggi catalogati per categoria in modo leggibile.
    """
    for category, items in categorized.items():
        print(f"\n=== {category} ===")
        if not items:
            print("  (nessun messaggio)")
            continue

        for entry in items:
            print(f"  Blocco {entry['block_height']}, Messaggio {entry['messaggio_n']}:")
            print(f"    {entry['contenuto']}")
