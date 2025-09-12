# ProgettoCrypto

Un progetto in Python per esplorare i messaggi lasciati dai miner nei blocchi Bitcoin.  
L’idea è di estrarre le **coinbase transactions** e gli output di tipo **OP_RETURN**, che i miner usano per inserire messaggi o segnalazioni di aggiornamento.
Useremo 

## Obiettivo
- Recuperare i blocchi dalla blockchain.
- Identificare la **coinbase transaction** (sempre la prima nel blocco).
- Estrarre e decodificare:
  - il campo `coinbase` (hex → testo, se leggibile),
  - gli eventuali output `OP_RETURN` presenti nella transazione.
- Raccogliere i messaggi in un formato leggibile o strutturato (JSON/CSV).

## Specifiche tecniche
- **Linguaggio:** Python 3.11+  
- **Dipendenze:** `requests` (installare con `pip install requests`)  
- **Dati:** blocchi recuperati tramite API pubbliche da [mempool](https://mempool.space/it/).

## Funzioni disponibili

```text
ultimoBlocco() -> dict
```
Ritorna l'ultimo blocco minato dalla blockchain tramite API mempool.

```text
stampaBlocco(block: dict) -> None
```
Stampa a video i dati principali di un blocco (altezza, id, timestamp, numero transazioni, miner).

```text
stampaHeader(block: dict) -> None
```
Mostra a video l'header del blocco, convertendo anche la versione in formato binario.

```text
listaUltimiNBlocchi(n: int) -> list
```
Recupera gli ultimi n blocchi partendo dall'ultimo e andando a ritroso.

```text
listaBlocchiTotale() -> list
```
Raccoglie tutti i blocchi della blockchain a partire dall'ultimo fino al genesis.

```text
stampaListaBlocchi(blocks: list) -> None
```
Stampa in sequenza i dettagli di una lista di blocchi.

```text
getTransazioni(block_hash: str) -> list
```
Restituisce la lista di transazioni associate a un blocco.

```text
getCoinbase(block_hash: str) -> dict
```
Estrae la prima transazione di un blocco (coinbase transaction).

```text
getCoinbaseDaBlocchi(lista_blocchi: list) -> list
```
Restituisce le coinbase transaction di tutti i blocchi forniti in input.

```text
stampaTransazioni(txs: list) -> None
```
Stampa in maniera leggibile le transazioni di un blocco (input, output e OP_RETURN).

```text
dettagliTransazione(txid: str) -> dict
```
Recupera i dettagli completi di una transazione a partire dal suo ID.

```text
estraiMessaggiMiner(lista_blocchi: list) -> list
```
Estrae e raccoglie i messaggi OP_RETURN dai blocchi forniti.

```text
stampaMessaggiMiner(risultati: list) -> None
```
Mostra a video i messaggi OP_RETURN trovati nei blocchi.

```text
stampaMessaggiMinerSuFile(risultati: list, filename: str = "messaggi_miner.txt") -> None
```
Stampa i messaggi dei miner e li salva su file.

```text
toBinary(n: int) -> str
```
## Esecuzione (esempio minimo)

Clona il repository:

```bash
git clone ht6tps://github.com/tuo-username/ProgettoCrypto.git
cd ProgettoCrypto
```

quindi per eseguire
```bash
python main.py
```
