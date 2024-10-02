# Affine Cipher

The **Affine Cipher** is a type of substitution cipher that uses mathematical functions for encryption and decryption. It involves two keys, `a` and `b`, to transform the plaintext.

## Encryption Formula
The encryption function for the affine cipher is given by:

$
C(x) = (a \cdot x + b) \, \mod \, m
$

Where:
- `E(x)` is the encrypted character.
- `x` is the numerical representation of the plaintext character.
- `a` and `b` are the keys used for encryption.
- `m` is the size of the alphabet (for the English alphabet,  $m = 26$ ).

## Decryption Formula
To decrypt, the following function is used:

$
D(x) = a^{-1} \cdot (x - b) \, \mod \, m
$

Where:
- $a^{-1}$ is the modular inverse of `a` modulo `m`.

## Example
If we choose `a = 5` and `b = 8` for the English alphabet (where $ m = 26 $):
- To encrypt the letter "C" (which corresponds to $x = 2$):
  $
  E(2) = (5 \cdot 2 + 8) \mod 26 = 18
  $
  The result, 18, corresponds to the letter "S", so "C" becomes "S".

## Note
> The keys `a` and `m` must be coprime (i.e., $ \gcd(a, m) = 1 $) to ensure that the encryption can be reversed during decryption.
