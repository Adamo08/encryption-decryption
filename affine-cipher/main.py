def mod_inverse(a, m):
    # Ensure a and m are coprime
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Function to encrypt plaintext using the Affine Cipher
def affine_encrypt(plaintext, a, b):
    result = ''
    m = 26  # Size of the alphabet

    for char in plaintext:
        # Encrypt only alphabetic characters
        if char.isalpha():
            # Convert to uppercase to simplify calculations
            char = char.upper()
            # Convert char to numerical value (A=0, B=1, ..., Z=25)
            x = ord(char) - ord('A')
            # Apply encryption formula: E(x) = (a * x + b) % m
            encrypted_char = (a * x + b) % m
            # Convert back to letter and append to result
            result += chr(encrypted_char + ord('A'))
        else:
            result += char  # Non-alphabet characters remain unchanged

    return result

# Function to decrypt ciphertext using the Affine Cipher
def affine_decrypt(ciphertext, a, b):
    result = ''
    m = 26  # Size of the alphabet
    a_inv = mod_inverse(a, m)  # Find modular inverse of a

    if a_inv is None:
        return "Decryption not possible. 'a' and 'm' must be coprime."

    for char in ciphertext:
        # Decrypt only alphabetic characters
        if char.isalpha():
            # Convert to uppercase to simplify calculations
            char = char.upper()
            # Convert char to numerical value (A=0, B=1, ..., Z=25)
            x = ord(char) - ord('A')
            # Apply decryption formula: D(x) = a_inv * (x - b) % m
            decrypted_char = (a_inv * (x - b)) % m
            # Convert back to letter and append to result
            result += chr(decrypted_char + ord('A'))
        else:
            result += char  # Non-alphabet characters remain unchanged

    return result


if __name__ == "__main__":
    
    plaintext = "HELLO ADAMO, HAVE A NICE DAY."
    
    a = 3
    b = 2

    # Encrypt the plaintext
    encrypted_text = affine_encrypt(plaintext, a, b)
    print(f"Encrypted: {encrypted_text}")

    # Decrypt the ciphertext
    decrypted_text = affine_decrypt(encrypted_text, a, b)
    print(f"Decrypted: {decrypted_text}") # Will the print the original text
