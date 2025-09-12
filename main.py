from utilityBlocco import stampaListaBlocchi, listaBlocchiTotale, ultimoBlocco, stampaBlocco, stampaHeader, listaUltimiNBlocchi
from utilityTransazioni import getTransazioni, stampaTransazioni, dettagliTransazione, getCoinbase, getCoinbaseDaBlocchi
from utility import toBinary
from utilityMinerMessage import stampaMessaggiMiner, stampaMessaggiMinerSuFile, estraiMessaggiMiner
from tqdm import tqdm

# recupera i blocchi
blocchi = listaUltimiNBlocchi(50)

# estrai dai blocchi i messaggi dei miner con barra
risultati = []
for block in tqdm(blocchi, desc="Analizzando blocchi", unit="blocco"):
    risultati_block = estraiMessaggiMiner([block])  # estraiMessaggiMiner lavora su lista
    risultati.extend(risultati_block)

# Stampa e salva su file
stampaMessaggiMinerSuFile(risultati)
