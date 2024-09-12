def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i.islower():
            number = ord(i) + shift
            if number > ord("z"):
                number -= 26
            ciphertext += chr(number)
        elif i.isupper():
            number = ord(i) + shift
            if number > ord("Z"):
                number -= 26
            ciphertext += chr(number)
        else:
            ciphertext += i

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i.islower():
            number = ord(i) - shift
            if number < ord("a"):
                number += 26
            plaintext += chr(number)
        elif i.isupper():
            number = ord(i) - shift
            if number < ord("A"):
                number += 26
            plaintext += chr(number)
        else:
            plaintext += i

    return plaintext
