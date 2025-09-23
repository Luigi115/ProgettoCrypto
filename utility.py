import string

#porta in binario
def toBinary(n):
    return bin(n)[2:]

#decodifica messaggio da esadecimale
def decode_hex_to_text(hex_str):
    try:
        return bytes.fromhex(hex_str).decode('utf-8', errors='ignore')
    except Exception:
        return hex_str
    

def filtra_ascii(text):
    return ''.join(c for c in text if c in string.printable)