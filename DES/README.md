# DES Encryption Algorithm

This repository contains a Python implementation of the **Data Encryption Standard (DES)** algorithm. DES is a symmetric-key block cipher that encrypts data in 64-bit blocks using a 56-bit key. This guide explains how the DES encryption process works and walks through the steps implemented in the Python script.

## Table of Contents

- [Overview](#overview)
- [Phase I: Key Preparation](#phase-i-key-preparation)
- [Phase II: Subkey Generation](#phase-ii-subkey-generation)
- [Phase III: Message Processing](#phase-iii-message-processing)
- [Phase IV: DES Rounds](#phase-iv-des-rounds)
- [Phase V: Final Permutation](#phase-v-final-permutation)
- [How to Run](#how-to-run)

---

## Overview

The DES encryption process consists of the following steps:
1. **Initial Permutation**: The message block is permuted according to a predefined table.
2. **16 Rounds of Encryption**: The message is divided into two halves and undergoes 16 rounds of the Feistel function, where a series of substitutions, permutations, and XOR operations take place.
3. **Final Permutation**: The message is permuted once more after the 16 rounds to produce the final ciphertext.

### Key Concepts
- **64-bit Input Message (M)**: The plaintext message block to be encrypted.
- **56-bit Key (K)**: The encryption key that drives the cipher. After permutation and shifts, it generates 16 subkeys.
- **Initial Permutation (IP)**: Rearranges the bits of the message before encryption.
- **Final Permutation (FP)**: A final rearrangement of bits after the encryption rounds.

---

## Phase I: Key Preparation

In this phase, the 64-bit encryption key is permuted and prepared for subkey generation.

### Steps:
1. **Key Input**: The key `K = 0x0f1571c947d9e859` is converted to a 64-bit binary string.
2. **Permutation Choice 1 (PC1)**: The 64-bit key is permuted using a predefined table, reducing it to a 56-bit key.
3. **Key Split**: The 56-bit key is split into two 28-bit halves: `C0` and `D0`.

---

### Phase II: Subkey Generation

Using the split key parts `C0` and `D0`, we apply circular left shifts to generate 16 new key pairs, `Cn` and `Dn`, for each round. The shifts are defined by the following table:

```python
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
```

After applying the shifts, we generate the subkeys using **Permutation Choice 2 (PC2)** to reduce the 56-bit combined key back to 48 bits.

```python
PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]
```

**KMAP**: This dictionary contains the 56-bit intermediate key values before applying PC2.

**ActualKMAP**: After applying PC2 to `KMAP`, we get 16 final subkeys of 48 bits, stored in `ActualKMAP`. These subkeys are used in each round of the encryption process.

```python
ActualKMAP = {
    round_num: ''.join(KMAP[round_num][i - 1] for i in PC2)
    for round_num in KMAP
}
```
---

## Phase III: Message Processing

The input message `M = 0x02468aceeca86420` is prepared for encryption.

### Steps:
1. **Initial Permutation (IP)**: The message is permuted according to the **Initial Permutation** table, producing two halves: `L0` and `R0`.
   
```python
PM = initial_permutation(MB)
L0, R0 = PM[:32], PM[32:]
```

---

## Phase IV: DES Rounds

In this phase, the message undergoes 16 rounds of encryption, where each round applies a Feistel function to the data.

### Steps:
1. **Expansion**: The 32-bit right half `R0` is expanded to 48 bits using the expansion table `E`.
2. **XOR Operation**: The expanded right half is XORed with the corresponding subkey from `KMAP`.
3. **Substitution (S-boxes)**: The XOR result is divided into 8 blocks of 6 bits, and each block is substituted using the predefined **S-boxes**. This reduces the result back to 32 bits.
4. **Permutation (P-box)**: The substituted result is permuted again using a **Permutation (P)** table.
5. **Swapping**: After each round, the left and right halves (`L` and `R`) are swapped, with the new right half being the result of the XOR operation with the previous left half.

This process repeats for 16 rounds, producing the final halves `L16` and `R16`.

```python
combined = des_encrypt(L0, R0, ActualKMAP)
```

---

## Phase V: Final Permutation

After 16 rounds of encryption, the two halves `L16` and `R16` are concatenated and passed through the **Final Permutation (FP)** table. This gives the final ciphertext.

```python
final_result = final_permutation(combined)
```

The result is converted from binary to hexadecimal to obtain the encrypted message.

---

## How to Run

1. Clone the repository and ensure you have Python installed.
2. Copy the provided Python script and execute it.
3. The encrypted message will be printed as output.

### Example Output:

```
Encrypted message: DA02CE3A89ECAC3B
```

---

## Notes

- This is a simple implementation for educational purposes.
- The DES algorithm is no longer considered secure for sensitive information due to its relatively short key length (56 bits).
- This implementation uses hardcoded values for the key and message but can easily be modified for other inputs.
