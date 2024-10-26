# Hill Cipher Implementation

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Encryption Process](#encryption-process)
- [Decryption Process](#decryption-process)
- [Key Matrix and Inverses](#key-matrix-and-inverses)
- [Usage](#usage)
- [Example](#example)
- [Limitations](#limitations)
- [References](#references)

---

## Introduction

The **Hill Cipher** is a polygraphic substitution cipher that encrypts blocks of plaintext letters using linear algebra. It was invented by the mathematician **Lester S. Hill** in 1929. The cipher uses a square matrix as the encryption key to transform blocks of plaintext into ciphertext.

This implementation of the Hill Cipher performs both encryption and decryption using a user-specified key matrix and plaintext.

Here’s how you can incorporate the **Hill Cipher** formula and a 3x3 matrix example using mathematical expressions in GitHub-supported markdown.

### Hill Cipher Formula

The encryption process can be represented mathematically as:

$$
C = E(K, P) = (P \cdot K) \mod 26
$$

Where:
- $C$ is the ciphertext (as a vector),
- $P$ is the plaintext (as a vector),
- $K$ is the key matrix,
- $\cdot$ denotes matrix multiplication,
- $\mod 26$ ensures the result wraps within the range of the alphabet.

### Example with a 3x3 Key Matrix

Let’s consider an example where:

- Plaintext vector 

$$
P = \begin{bmatrix} 15 \\ 0 \\ 24 \end{bmatrix} \quad \text{(which corresponds to the letters "PAY")}
$$

- Key matrix 

$$
K = \begin{bmatrix} 
17 & 17 & 5 \\ 
21 & 18 & 21 \\ 
2 & 2 & 19 
\end{bmatrix}
$$

The encryption process is:

$$
C = \left( \begin{bmatrix} 15 \\ 0 \\ 24 \end{bmatrix} \cdot \begin{bmatrix} 
17 & 17 & 5 \\ 
21 & 18 & 21 \\ 
2 & 2 & 19 
\end{bmatrix} \right) \mod 26
$$

First, compute the matrix multiplication:

$$
\begin{bmatrix} 15 \\ 0 \\ 24 \end{bmatrix} \cdot \begin{bmatrix} 
17 & 17 & 5 \\ 
21 & 18 & 21 \\ 
2 & 2 & 19 \end{bmatrix} 
= \begin{bmatrix} 
(15 \cdot 17) + (0 \cdot 21) + (24 \cdot 2) \\ 
(15 \cdot 17) + (0 \cdot 18) + (24 \cdot 2) \\ 
(15 \cdot 5) + (0 \cdot 21) + (24 \cdot 19) 
\end{bmatrix} 
= \begin{bmatrix} 
303 \\ 
303 \\ 
531 
\end{bmatrix}
$$

Now, apply $\mod 26$:

$$
C = \begin{bmatrix} 
303 \mod 26 \\ 
303 \mod 26 \\ 
531 \mod 26 
\end{bmatrix} = \begin{bmatrix} 
17 \\ 
17 \\ 
11 
\end{bmatrix}
$$

Finally, convert the result to letters (0 = A, 1 = B, ..., 25 = Z):

- 17 corresponds to 'R',
- 11 corresponds to 'L'.

So, the ciphertext for "PAY" is **"RRL"**.

---

## Prerequisites

To successfully run this implementation, you need:
- Basic knowledge of linear algebra (matrix multiplication, determinants, and inverses).
- Understanding of modular arithmetic (mod 26 for working with the English alphabet).

**Dependencies:**
- Python 3.x
- NumPy (for matrix operations)

```bash
pip install numpy
```

## Encryption Process

1. **Plaintext Preparation**: 
    - Convert the plaintext into numerical values (A=0, B=1, ..., Z=25).
    - Group the plaintext into blocks of size equal to the key matrix dimension.
    - If the last block is incomplete, pad it with filler characters (commonly 'X').

2. **Matrix Multiplication**:
    - Each block is represented as a column vector.
    - Multiply the key matrix by the plaintext vector (mod 26).

3. **Ciphertext Generation**:
    - Convert the resulting numerical values back into letters to form the ciphertext.

## Decryption Process

1. **Inverse Key Matrix**:
    - To decrypt, you need the inverse of the key matrix (mod 26).
    - If the key matrix has no modular inverse, decryption is not possible with that key.

2. **Matrix Multiplication**:
    - Multiply the inverse key matrix by the ciphertext blocks (mod 26) to retrieve the original plaintext.

3. **Plaintext Retrieval**:
    - Convert the resulting numbers back into letters to retrieve the decrypted plaintext.

---

## Key Matrix and Inverses

- The key matrix must be invertible modulo 26. This means its determinant (mod 26) must not be 0, and it must have a multiplicative inverse modulo 26.
- The determinant and inverse can be calculated using linear algebra techniques and modular arithmetic.

### Example Key Matrix

For a $3 \times 3$ key matrix $K$:

$$
K = \begin{bmatrix}
17 & 17 & 5 \\
21 & 18 & 21 \\
2 & 2 & 19
\end{bmatrix}
$$

### Inverse Key Matrix

The inverse of the key matrix $K$ modulo 26 is given by:

$$
K^{-1} = \begin{bmatrix}
4 & 9 & 15 \\
15 & 17 & 6 \\
24 & 0 & 17
\end{bmatrix}
$$

### Properties

- **Determinant**: To verify that $K$ is invertible, calculate the determinant of $K$. If the determinant is not congruent to 0 modulo 26, then $K$ is invertible.
- **Inverse Calculation**: The inverse $K^{-1}$ can be computed using methods such as the adjugate matrix and the multiplicative inverse of the determinant modulo 26.

This example demonstrates how a specific key matrix $K$ and its inverse $K^{-1}$ are structured in the context of the Hill Cipher.

---

## Usage

### 1. Encryption

Run the program and specify:
- Plaintext to encrypt.
- The key matrix to use for encryption.

### 2. Decryption

Run the program and specify:
- Ciphertext to decrypt.
- The key matrix used during encryption.

### Code Structure:

```bash
hill_cipher.py         # Main Python script for encryption and decryption
README.md              # This file, explaining the Hill Cipher implementation
```

### Functions:

1. **`encrypt(plaintext, key_matrix)`**: Encrypts the given plaintext using the provided key matrix.
2. **`decrypt(ciphertext, key_matrix)`**: Decrypts the given ciphertext using the provided key matrix.
3. **`mod_inverse(matrix)`**: Computes the modular inverse of the key matrix.

## Example

### Encryption:

```python
plaintext = "PAYMOREMONEY"
key_matrix = [
                [17,17,5],
                [21,18,21],
                [2,2,19]
            ]  # 3x3 key matrix

# Encrypt plaintext
ciphertext = encrypt(plaintext, key_matrix)
print("Ciphertext:", ciphertext)
```

### Decryption:

```python
ciphertext = "LNSHDLEWMTRW"
key_matrix = [
                [17,17,5],
                [21,18,21],
                [2,2,19]
            ]  # 3x3 key matrix

# Decrypt ciphertext
decrypted_text = decrypt(ciphertext, key_matrix)
print("Decrypted Text:", decrypted_text)
```

## Limitations

- The key matrix must be invertible mod 26, which restricts the choice of key matrices.
- The Hill cipher is vulnerable to known-plaintext attacks if the attacker knows part of the plaintext and its corresponding ciphertext.

## References

1. Hill, L. S. (1929). Cryptography in an Algebraic Alphabet. *The American Mathematical Monthly*.
2. [Hill Cipher - Wikipedia](https://en.wikipedia.org/wiki/Hill_cipher)

--- 