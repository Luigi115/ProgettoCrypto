# ProgettoCrypto

Un progetto in Python per esplorare i messaggi lasciati dai miner nei blocchi Bitcoin.  
L’idea è di estrarre le **coinbase transactions** e gli output di tipo **OP_RETURN**, che i miner usano per inserire messaggi o segnalazioni di aggiornamento.

## 📑 Indice

- [ProgettoCrypto](#progettocrypto)
- [Obiettivo](#obiettivo)
- [Specifiche tecniche](#specifiche-tecniche)
- [Funzioni disponibili](#funzioni-disponibili)
- [Esecuzione (esempio minimo)](#esecuzione-esempio-minimo)

## Obiettivo
- Recuperare i blocchi dalla blockchain.
- Identificare la **coinbase transaction** (sempre la prima nel blocco).
- Estrarre e decodificare:
  - il campo `coinbase` (hex → testo, se leggibile),
  - gli eventuali output `OP_RETURN` presenti nella transazione.
- Raccogliere i messaggi in un formato leggibile o strutturato (JSON/CSV).

## Specifiche tecniche
- **Linguaggio:** Python 3.11+  
- **Dipendenze:** `requests`, `tqdm` (installare con `pip install requests tqdm`)  
- **Dati:** blocchi recuperati tramite API pubbliche da [mempool](https://mempool.space/it/).

## Funzioni disponibili

### Utility generali
- `toBinary(n: int) -> str` : converte un numero in binario (senza prefisso `0b`).  
- `decode_hex_to_text(hex_str: str) -> str` : decodifica un messaggio esadecimale in testo UTF-8, ignora errori.

### Blocco singolo
- `ultimoBlocco() -> dict` : ritorna l'ultimo blocco minato dalla blockchain tramite API mempool.  
- `stampaBlocco(block: dict) -> None` : stampa a video i dati principali di un blocco (altezza, id, timestamp, numero transazioni, miner).  
- `stampaHeader(block: dict) -> None` : mostra a video l'header del blocco, convertendo la versione in formato binario.

### Lista blocchi
- `listaUltimiNBlocchi(n: int) -> list` : recupera gli ultimi n blocchi partendo dall'ultimo e andando a ritroso.  
- `listaBlocchiTotale() -> list` : raccoglie tutti i blocchi della blockchain a partire dall'ultimo fino al genesis.  
- `stampaListaBlocchi(blocks: list) -> None` : stampa in sequenza i dettagli di una lista di blocchi.

### Transazioni
- `getTransazioni(block_hash: str) -> list` : restituisce la lista di transazioni associate a un blocco.  
- `getCoinbase(block_hash: str) -> dict` : estrae la prima transazione di un blocco (coinbase transaction).  
- `getCoinbaseDaBlocchi(lista_blocchi: list) -> list` : restituisce le coinbase transaction di tutti i blocchi forniti in input, includendo id e altezza del blocco.  
- `stampaTransazioni(txs: list) -> None` : stampa in maniera leggibile le transazioni di un blocco (input, output e OP_RETURN).

### OP_RETURN e messaggi miner
- `estraiOpReturn(tx: dict) -> list` : estrae tutti gli output OP_RETURN da una transazione.  
- `estraiOpReturnDaTransazioni(transazioni: list) -> list` : estrae tutti gli OP_RETURN da una lista di transazioni, includendo info sul blocco.  
- `filtraOpReturnPerBlocco(lista_blocchi: list) -> list` : restituisce solo block_height e lista OP_RETURN di ogni blocco.  
- `stampaOpReturnPerBlocco(lista_blocchi: list) -> None` : stampa a video gli OP_RETURN per blocco.  
- `estraiOpReturnJSON(tx: dict) -> dict` : decodifica gli OP_RETURN e li restituisce in formato JSON.

## Come installare

Clona il repository ed esegui il progetto:

```bash
git clone https://github.com/tuo-username/ProgettoCrypto.git
```

```bash
cd ProgettoCrypto
python main.py
```