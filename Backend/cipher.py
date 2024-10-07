

def encrypt(text, n, d):
    encryptedText = ""
    for char in text:
        if (char != " ") or (char != "!"):
            key = ord(char)
            key = key + (d * n) - 34
            if key >= 0:
                key = (key % 93) + 34
            else:
                key = ((key + 93) % 93) + 34
            key = chr(key)
            encryptedText = key + encryptedText
    return encryptedText
    
def decrypt(text, n, d):
    decryptedText = ""
    for char in text:
        key = ord(char)
        if (char != " ") or (char != "!"):
            key = key - (d * n) - 34
            if key >= 0:
                key = (key % 93) + 34
            else:
                key = ((key + 93) % 93) + 34
        key = chr(key)
        decryptedText = key +decryptedText
    return decryptedText
