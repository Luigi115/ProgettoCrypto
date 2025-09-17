from utilityBlocco import stampaListaBlocchi, listaBlocchiTotale, ultimoBlocco, stampaBlocco, stampaHeader, listaUltimiNBlocchi
from utilityTransazioni import getTransazioni, stampaTransazioni, getCoinbase, getCoinbaseDaBlocchi
from utility import toBinary
from utilityMinerMessage import estraiOpReturn, estraiOpReturnJSON
from tqdm import tqdm

# Prendi l'ultimo blocco
blocco = ultimoBlocco()
coinbase_tx = getCoinbase(blocco["id"])

# Estrai e decodifica OP_RETURN in JSON
op_json = estraiOpReturnJSON(coinbase_tx)

# Stampa il risultato
import json
print(json.dumps(op_json, indent=2))