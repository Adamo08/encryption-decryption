# Vigenère Cipher

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

## Overview
The **Vigenère Cipher** is a method of encrypting alphabetic text by using a keyword to shift each letter in the message. It is a form of polyalphabetic substitution that provides more security compared to the Caesar Cipher by using different shifts based on the keyword. This implementation encrypts and decrypts text with the Vigenère Cipher using a provided keyword.

## Features
- Encrypts and decrypts messages using the Vigenère cipher.
- Customizable keyword for encryption and decryption.
- Supports both uppercase and lowercase letters.
- Ignores non-alphabetic characters (like punctuation and spaces).
- Provides a simple Python implementation.

## How It Works
The Vigenère Cipher uses a key that repeats to match the length of the message. The encryption is performed by shifting each letter of the plaintext by the position of the corresponding letter in the key. The decryption reverses this process.

### Encryption:
1. The key is repeated to match the length of the plaintext.
2. Each letter in the plaintext is shifted forward in the alphabet by the position of the corresponding letter in the key.

### Decryption:
1. The key is repeated to match the length of the ciphertext.
2. Each letter in the ciphertext is shifted backward in the alphabet by the position of the corresponding letter in the key, returning the original plaintext.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/vigenere-cipher.git
    ```

2. Navigate to the project directory:
    ```bash
    cd vigenere-cipher
    ```


## Usage
You can use the provided Python functions to encrypt and decrypt messages. The `encrypt_vigenere` and `decrypt_vigenere` functions both require a message and a keyword.

### Example Usage
Here is how you can use the Vigenère Cipher in a Python script:

```python
text_to_encrypt = "Hello, World!"
key = "KEY"

# Encrypt the message
encrypted_text = encrypt_vigenere(text_to_encrypt, key)
print(f"Encrypted Text: {encrypted_text}")

# Decrypt the message
decrypted_text = decrypt_vigenere(encrypted_text, key)
print(f"Decrypted Text: {decrypted_text}")
```


### Functions:
- `generate_key(msg, key)`: Generates the key by repeating or trimming it to match the length of the message.
- `encrypt_vigenere(msg, key)`: Encrypts the message using the Vigenère Cipher.
- `decrypt_vigenere(msg, key)`: Decrypts the message using the Vigenère Cipher.

## Examples
### Encryption Example:
- **Plaintext**: `Hello, World!`
- **Keyword**: `KEY`
- **Encrypted Text**: `RIJVS UYVJN`

### Decryption Example:
- **Ciphertext**: `RIJVS UYVJN`
- **Keyword**: `KEY`
- **Decrypted Text**: `Hello, World!`