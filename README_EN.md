# ProgettoCrypto

A Python project to explore messages left by miners in Bitcoin blocks.  
The idea is to extract **coinbase transactions** and **OP_RETURN** outputs, which miners use to embed messages or update signals.

## 📑 Table of Contents

- [ProgettoCrypto](#progettocrypto)
- [Objective](#objective)
- [Technical Specifications](#technical-specifications)
- [Available Functions](#available-functions)
- [Installation and Usage](#installation-and-usage)

## Objective
- Retrieve blocks from the blockchain.
- Identify the **coinbase transaction** (always the first transaction in a block).
- Extract and decode:
  - the `coinbase` field (hex → readable text, if possible),
  - any `OP_RETURN` outputs present in the transaction.
- Collect messages in a readable or structured format (JSON/CSV).

## Technical Specifications
- **Language:** Python 3.11+  
- **Dependencies:** `requests`, `tqdm` (install with `pip install requests tqdm`)  
- **Data:** blocks retrieved via public APIs from [mempool](https://mempool.space/en/).

## Available Functions

### General Utilities
- `toBinary(n: int) -> str` : converts a number to binary (without the `0b` prefix).  
- `decode_hex_to_text(hex_str: str) -> str` : decodes a hexadecimal message into UTF-8 text, ignoring errors.

### Single Block
- `ultimoBlocco() -> dict` : returns the last mined block from the blockchain via mempool API.  
- `stampaBlocco(block: dict) -> None` : prints the main details of a block (height, id, timestamp, number of transactions, miner).  
- `stampaHeader(block: dict) -> None` : displays the block header, including the binary version.

### Block List
- `listaUltimiNBlocchi(n: int) -> list` : retrieves the last n blocks starting from the latest and going backward.  
- `listaBlocchiTotale() -> list` : collects all blocks from the blockchain from the latest down to the genesis block.  
- `stampaListaBlocchi(blocks: list) -> None` : prints the details of a list of blocks sequentially.

### Transactions
- `getTransazioni(block_hash: str) -> list` : returns the list of transactions in a block.  
- `getCoinbase(block_hash: str) -> dict` : extracts the first transaction of a block (coinbase transaction).  
- `getCoinbaseDaBlocchi(lista_blocchi: list) -> list` : returns the coinbase transactions of all input blocks, including block id and height.  
- `stampaTransazioni(txs: list) -> None` : prints the transactions of a block in a readable format (inputs, outputs, and OP_RETURN).

### OP_RETURN and Miner Messages
- `estraiOpReturn(tx: dict) -> list` : extracts all OP_RETURN outputs from a transaction.  
- `estraiOpReturnDaTransazioni(transazioni: list) -> list` : extracts all OP_RETURN outputs from a list of transactions, including block info.  
- `filtraOpReturnPerBlocco(lista_blocchi: list) -> list` : returns only block_height and OP_RETURN list for each block.  
- `stampaOpReturnPerBlocco(lista_blocchi: list) -> None` : prints OP_RETURN messages for each block.  
- `estraiOpReturnJSON(tx: dict) -> dict` : decodes OP_RETURN outputs and returns them as JSON.

## Installation and Usage

Clone the repository and run the project:

```bash
git clone https://github.com/tuo-username/ProgettoCrypto.git
```

```bash
cd ProgettoCrypto
python main.py
```