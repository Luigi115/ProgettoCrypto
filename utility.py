def toBinary(n):
    return bin(n)[2:]

#decodifica messaggio da esadecimale
def decode_hex_to_text(hex_str):
    try:
        return bytes.fromhex(hex_str).decode('utf-8', errors='ignore')
    except Exception:
        return hex_str