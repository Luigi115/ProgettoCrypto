from tqdm import tqdm
from utility import toBinary, decode_hex_to_text, filtra_ascii
from utilityTransazioni import getCoinbase
import string
import matplotlib.pyplot as plt
import numpy as np

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
            print(f"  Blocco {entry['block_height']}, Messaggio {entry['messaggio_n']}: {entry['contenuto']}")



def analizza_opreturn(dati):
    # 'dati' è il dizionario categorizzato: {'CORE': [{...}], 'RSKBLOCK': [{...}], ...}
    
    # Inizializza i contatori necessari
    totali_per_blocco_dict = {}
    categorie_counter = {} # Useremo un dizionario per il conteggio totale delle categorie

    # 1. Raggruppa i messaggi per Blocco (Block Height) e conta le categorie
    # Questo loop risolve il problema del NameError e del Grafico 1
    for categoria, items in dati.items():
        # Conteggio per il Grafico 2 (Torta)
        categorie_counter[categoria] = len(items) 

        # Itera su tutti i messaggi per contare gli OP_RETURN per Blocco
        for item in items:
            # Assicurati che l'elemento abbia 'block_height'
            height = item.get('block_height')
            if height is not None:
                # Conteggio per il Grafico 1 (Barre): raggruppa per Block Height
                totali_per_blocco_dict[height] = totali_per_blocco_dict.get(height, 0) + 1

    # 2. Prepara le liste per il Grafico 1 (Barre)
    # Ordina i blocchi per Block Height per un grafico coerente
    blocchi_ordinati = sorted(totali_per_blocco_dict.items())

    # Prepara le liste finali per Matplotlib
    labels_blocchi = [str(height) for height, total in blocchi_ordinati]
    totali_per_blocco = [total for height, total in blocchi_ordinati]

    # --- Analisi e Stampa ---

    # Statistiche base
    if not totali_per_blocco:
        print("Nessun OP_RETURN trovato nei dati forniti.")
        return # Esci se non ci sono dati
        
    media = sum(totali_per_blocco) / len(totali_per_blocco)
    print(f"Numero medio di OP_RETURN per blocco: {media:.2f}")

    # Distribuzione per blocco (stampa)
    print("\nDistribuzione OP_RETURN per Blocco:")
    for height, totale in zip(labels_blocchi, totali_per_blocco):
        print(f"Blocco {height}: {totale} OP_RETURN")
    
    # --------------------------------------------------------------------------
    ## 🔹 Grafico 1: OP_RETURN per blocco (bar chart)
    # --------------------------------------------------------------------------
    x = np.arange(len(totali_per_blocco))
    plt.figure(figsize=(10,5))
    bars = plt.bar(x, totali_per_blocco, color="skyblue", edgecolor="black")
    plt.axhline(media, color="red", linestyle="--", label=f"Media = {media:.2f}")
    plt.xlabel("Block Height")
    plt.ylabel("Numero OP_RETURN")
    plt.title("Numero di OP_RETURN per blocco")
    
    # Imposta le etichette con rotazione
    plt.xticks(x, labels_blocchi, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()

    # Annotazioni sopra le barre
    for bar in bars:
        h = bar.get_height()
        plt.annotate(f'{int(h)}',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom')

    plt.show()

    # --------------------------------------------------------------------------
    ## 🔹 Grafico 2: Distribuzione per categorie (torta)
    # --------------------------------------------------------------------------
    
    # Rimuovi le categorie con conteggio zero prima di plottare
    categorie_totali_filtrate = {k: v for k, v in categorie_counter.items() if v > 0}
    
    if sum(categorie_totali_filtrate.values()) > 0:
        labels_cat = list(categorie_totali_filtrate.keys())
        sizes = list(categorie_totali_filtrate.values())
        
        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels_cat, autopct='%1.1f%%', startangle=140)
        plt.title("Distribuzione OP_RETURN per categoria")
        plt.tight_layout()
        plt.show()