import numpy as np

def mod26(matrix):
    """Applies modulo 26 to all elements of a numpy array or matrix."""
    return np.mod(matrix, 26)

def matrix_multiply(a, b):
    """Multiplies two matrices and returns the result."""
    return np.dot(a, b)

def text_to_vector(text):
    """Converts a string of text into a vector of numbers (A=0, B=1, ..., Z=25)."""
    return [ord(char) - ord('A') for char in text.upper() if char.isalpha()]

def vector_to_text(vector):
    """Converts a vector of numbers back to a string of text (0=A, 1=B, ..., 25=Z)."""
    return ''.join(chr(num + 65) for num in vector)

def mod_inverse(matrix, modulus):
    """Computes the modular inverse of a matrix under a specified modulus."""
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, modulus)  # Find modular inverse of determinant mod 26
    
    # Calculate adjugate matrix and apply mod 26
    matrix_inv = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    return mod26(matrix_inv)

def hill_encrypt(plaintext, key_matrix):
    """Encrypts the plaintext using the Hill cipher with the given key matrix."""
    matrix_size = key_matrix.shape[0]
    plaintext_vector = text_to_vector(plaintext)
    ciphertext = ""

    for i in range(0, len(plaintext_vector), matrix_size):
        block = plaintext_vector[i:i + matrix_size]

        # Pad only if this is the last block and not a full block size
        if len(block) < matrix_size:
            block += [23] * (matrix_size - len(block))  # padding with 'X' (23)
        
        # Convert block to numpy array, reshape to column vector
        block_matrix = np.array(block).reshape(matrix_size, 1)
        
        # Encrypt the block
        encrypted_block = mod26(matrix_multiply(key_matrix, block_matrix)).flatten()
        
        # Append encrypted block to ciphertext
        ciphertext += vector_to_text(encrypted_block)
    
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    """Decrypts the ciphertext using the Hill cipher with the given key matrix."""
    matrix_size = key_matrix.shape[0]
    ciphertext_vector = text_to_vector(ciphertext)
    key_matrix_inv = mod_inverse(key_matrix, 26)
    plaintext = ""

    for i in range(0, len(ciphertext_vector), matrix_size):
        block = ciphertext_vector[i:i + matrix_size]
        
        # Convert block to numpy array, reshape to column vector
        block_matrix = np.array(block).reshape(matrix_size, 1)
        
        # Decrypt the block
        decrypted_block = mod26(matrix_multiply(key_matrix_inv, block_matrix)).flatten()
        
        # Append decrypted block to plaintext
        plaintext += vector_to_text(decrypted_block)
    
    return plaintext

def main():
    # Define the plaintext string
    plaintext = "PAYMOREMONEY"
    
    # Define the key matrix (3x3 matrix)
    key_matrix = np.array([
        [17, 17, 5],
        [21, 18, 21],
        [2, 2, 19]
    ])
    
    # Encrypt the plaintext
    ciphertext = hill_encrypt(plaintext, key_matrix)
    print("Ciphertext:", ciphertext)

    # Decrypt the ciphertext
    decrypted_text = hill_decrypt(ciphertext, key_matrix)
    print("Decrypted Text:", decrypted_text)

if __name__ == "__main__":
    main()
