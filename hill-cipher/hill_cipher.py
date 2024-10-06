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

def hill_encrypt(plaintext, key_matrix):
    """Encrypts the plaintext using the Hill cipher with the given key matrix."""
    pass

def main():
    # Define the plaintext string
    plaintext = "PAY"  # This can be any string
    
    # Define the key matrix (3x3 matrix)
    key_matrix = np.array([
        [17, 17, 5],
        [21, 18, 21],
        [2, 2, 19]
    ])

    
    
    
if __name__ == "__main__":
    main()
