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

## Esecuzione (esempio minimo)

Clona il repository:

```bash
git clone https://github.com/tuo-username/ProgettoCrypto.git
cd ProgettoCrypto
```

quindi per eseguire
```bash
python main.py
```
