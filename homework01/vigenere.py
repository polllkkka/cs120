def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    add1 = 0
    while len(plaintext) > len(keyword):
        keyword += keyword[add1]
        add1 += 1
    for i in range(len(keyword)):
        if keyword[i].isupper():
            key = ord(keyword[i]) - 65  # 65-й элемент - A. А - сдвиг на 0.
        elif keyword[i].islower():
            key = ord(keyword[i]) - 97  # 97-й элемент - а.
        if plaintext[i].isalpha():
            el1 = ord(plaintext[i])
            if plaintext[i].isupper() and el1 >= 91 - key:
                ciphertext += chr(el1 - 26 + key)
            elif plaintext[i].islower() and el1 >= 123 - key:
                ciphertext += chr(el1 - 26 + key)
            else:
                ciphertext += chr(el1 + key)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    add = 0
    while len(ciphertext) > len(keyword):
        keyword += keyword[add]
        add += 1
    for i, _ in enumerate(keyword):
        if keyword[i].isupper():
            key = ord(keyword[i]) - 65
        elif keyword[i].islower():
            key = ord(keyword[i]) - 97
        if ciphertext[i].isalpha():
            el = ord(ciphertext[i])
            if ciphertext[i].isupper() and el <= 64 + key:
                plaintext += chr(el + 26 - key)
            elif ciphertext[i].islower() and el <= 96 + key:
                plaintext += chr(el + 26 - key)
            else:
                plaintext += chr(el - key)
        else:
            plaintext += ciphertext[i]
    return plaintext
