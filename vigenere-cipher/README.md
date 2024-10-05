# Vigenère Cipher with Auto-Key System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Key Management Problem](#key-management-problem)
- [Auto-Key System Enhancement](#auto-key-system-enhancement)
- [Usage](#usage)
- [Examples](#examples)

## Overview
The **Vigenère Cipher** is a method of encrypting alphabetic text using a keyword to shift each letter in the message. It’s a polyalphabetic substitution cipher that is more secure than the Caesar Cipher by utilizing different shifts based on a keyword. However, traditional key management introduces vulnerabilities that can be improved using the **Auto-Key System**.

This implementation offers encryption and decryption using both the traditional Vigenère cipher and an enhanced version with the **Auto-Key System** to strengthen security.

## Features
- Encrypts and decrypts messages using both traditional Vigenère cipher and the Auto-Key System.
- Customizable keyword for encryption and decryption.
- Supports both uppercase and lowercase letters.
- Ignores non-alphabetic characters (like punctuation and spaces).
- Provides a more secure Auto-Key System to reduce repetition vulnerabilities.

## How It Works
The Vigenère Cipher relies on a repeating key to determine how much each letter of the message is shifted. Traditionally, the key is repeated to match the length of the message. With the **Auto-Key System**, the key is extended by appending part of the message itself to the key, making the cipher more resilient to certain cryptographic attacks.

### Encryption:
1. The key is either repeated (in the traditional Vigenère cipher) or extended using the **Auto-Key System**.
2. Each letter in the plaintext is shifted forward in the alphabet by the position of the corresponding letter in the key.

### Decryption:
1. The key is repeated or extended to match the length of the ciphertext.
2. Each letter in the ciphertext is shifted backward in the alphabet by the position of the corresponding letter in the key, returning the original plaintext.

## Key Management Problem
In the traditional Vigenère Cipher, the keyword is repeated to match the length of the plaintext. This introduces a vulnerability: **key repetition**. If the keyword is short and the plaintext is long, the repeated key can be detected through frequency analysis, weakening the security of the cipher.

### Example:
- **Plaintext**: `HELLOWORLD`
- **Keyword**: `KEY`
- **Repeated Key**: `KEYKEYKEYK`

This repetition exposes patterns in the ciphertext, allowing cryptanalysts to perform statistical attacks and deduce the key.

## Auto-Key System Enhancement
To mitigate the problem of key repetition, we can use the **Auto-Key System**. Instead of repeating the key, we append the message itself to the key, reducing redundancy and making it harder to detect patterns.

### How Auto-Key Works:
1. **Initial Key**: The original keyword is used for the first part of the message.
2. **Auto-Key Extension**: After the keyword is exhausted, the remaining characters of the key are derived from the plaintext itself.

### Example:
- **Plaintext**: `HELLOWORLD`
- **Keyword**: `KEY`
- **Auto-Key**: `KEYHELLOWO`

This method ensures that the key is non-repetitive and unique for every message, significantly enhancing security against frequency analysis.

## Usage
You can use the provided Python functions to encrypt and decrypt messages with either the traditional Vigenère cipher or the Auto-Key system. The `encrypt_vigenere` and `decrypt_vigenere` functions both require a message and a keyword, while the `generate_auto_key` function allows you to apply the Auto-Key system for enhanced security.

### Example Usage with Auto-Key System:
```python
text_to_encrypt = "HELLOWORLD"
key = "KEY"

'''
    To test the autokey implementation, change the generate_key() 
    to generate_auto_key() inside encrypt_vigenere() and decrypt_vigenere() 
    functions
'''


# Encrypt the message with the auto-key
encrypted_text = encrypt_vigenere(text_to_encrypt, key)
print(f"Encrypted Text with Auto-Key: {encrypted_text}")

# Decrypt the message with the auto-key
decrypted_text = decrypt_vigenere(encrypted_text, auto_key)
print(f"Decrypted Text with Auto-Key: {decrypted_text}")
```

### Functions:
- `generate_key(msg, key)`: Generates the traditional repeated key by matching the message length.
- `generate_auto_key(msg, key)`: Generates an extended key using the Auto-Key System for enhanced security.
- `encrypt_vigenere(msg, key)`: Encrypts the message using the Vigenère Cipher.
- `decrypt_vigenere(msg, key)`: Decrypts the message using the Vigenère Cipher.

## Examples

### Traditional Vigenère Cipher Encryption Example:
- **Plaintext**: `HELLOWORLD`
- **Keyword**: `KEY`
- **Repeated Key**: `KEYKEYKEYK`
- **Encrypted Text**: `RIJVSUYVJN`

### Auto-Key System Encryption Example:
- **Plaintext**: `HELLOWORLD`
- **Keyword**: `KEY`
- **Auto-Key**: `KEYHELLOWO`
- **Encrypted Text**: `RIJVS UYVJN`

### Decryption Example:
- **Ciphertext**: `RIJVSUYVJN`
- **Auto-Key**: `KEYHELLOWO`
- **Decrypted Text**: `HELLOWORLD`
