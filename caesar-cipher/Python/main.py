def caesar_cipher_encrypt(text, shift):
    """Encrypts the text using the Caesar Cipher with the given shift (k)."""
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char  # Non-alphabet characters remain unchanged
    return result

def caesar_cipher_decrypt(text, shift):
    """Decrypts the text using the Caesar Cipher with the given shift."""
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            result += char  # Non-alphabet characters remain unchanged
    return result


text = input("Enter text: ")
shift = int(input("Enter shift value (key): "))

# Encrypt the text
encrypted_text = caesar_cipher_encrypt(text, shift)
print(f"Encrypted Text: {encrypted_text}")

# Decrypt the text
decrypted_text = caesar_cipher_decrypt(encrypted_text, shift)
print(f"Decrypted Text: {decrypted_text}") # Will show the original text
