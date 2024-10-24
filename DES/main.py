
'''
======================== PHASE I ========================
'''

K = 0x0f1571c947d9e859
M = 0x02468aceeca86420 # Message is one block (64 bits long)

# ==> Next step : K and M to Binary representaion

KB = bin(K)[2:].zfill(64)
MB = bin(M)[2:].zfill(64)

PC1 = [
    57, 49, 41, 33, 25, 17, 9,   # First 28 bits
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,

    63, 55, 47, 39, 31, 23, 15,  # Last 28 bits
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
] # 56-Bit


K_ = ''.join([KB[x-1] for x in PC1]) # 56-bit

# ==> Next Step : Split K_ to C0 and D0
[C0,D0] = [K_[0:28],K_[28:-1]]
# C0 , D0 are both 28-bits long
# ==> Next step : apply left shifts

'''
    left_shift() to apply the left shift by a number of shifts
'''
def left_shift(bits, num_shifts):
    """Left shifts a list of bits by num_shifts."""
    return bits[num_shifts:] + bits[:num_shifts]
    
'''
    apply_key_shifts(): The function that generates the 16 subkeys (Without applying PC-2)
'''    
def apply_key_shifts(C0, D0):
    """Applies left shifts for 16 DES rounds."""
    KMAP = {}  # Dictionary to store the round keys
    LF = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]  # Left shift table
    
    for i in range(16):
        # Perform the left shifts for each round
        C0 = left_shift(C0, LF[i]).zfill(28)
        D0 = left_shift(D0, LF[i]).zfill(28)
        
        # Display the current round's C and D values, padded with zeros to 28 bits
        print(f"Round {i+1}:\nC{i+1} = {C0}\nD{i+1} = {D0}\n\n")
        
        # Store the combined 56-bit result of C and D in KMAP for the current round
        KMAP[i+1] = C0 + D0  # Using i+1 to store keys 1 to 16
    
    return KMAP  # Return the map after all 16 rounds


KMAP = apply_key_shifts(C0,D0)

# Next-Step : is to apply the PC-2 to each key in the MAP to generate the actual keys from 1 to 16 , each is 48-bits long

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

ActualKMAP = {
    round_num: ''.join(combined_key[i - 1] for i in PC2)
    for round_num, combined_key in KMAP.items()
}

# The ActualKMAP contains the keys that will be used in the next phase

'''
======================== PHASE II ========================
'''


IP = [ 
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

# Initial Permutation       
PM = "".join([MB[x-1] for x in IP])
# Next Step : We split PM into L0 and R0
[L0,R0] = [PM[:32],PM[32:]]

'''
======================== PHASE III ========================
'''

'''
    + L(n) = R(n-1)
    + R(n) = L(n-1) ^ F[R(n-1),Kn]
    + F = ??
    
    ==> 
    + L1 = R0
    + R1 = L0 ^ F(R0,K1)
    .
    .
    .
'''

# F : function[R(i-1),Ki] => 
# 1. Expansion of R(i-1) with the E function (output: 48bits)
# 2. Then E[R(i-1)] ^ Ki ==> 48 bits long
# The we split the 48 bits into 8 boxes , each with 6 bits long
# B1+B2+B3+B4+B5+B6+B7+B8
# 3. Substitution/Choice with S-boxes
# S1(B1)+S2(B2)+S3(B3)....+S8(B8)
# Si(B(i)) is 4 bits long , So the result will be 8 * 4 = 32 bits output
# 4. Then an other permutation is performed to get the output F
# This output is the Function[R(i-1),Ki]

E = [
        32, 1, 2, 3, 4, 5, 
        4, 5, 6, 7, 8, 9, 
        8, 9, 10, 11, 12, 13, 
        12, 13, 14, 15, 16, 17, 
        16, 17, 18, 19, 20, 21, 
        20, 21, 22, 23, 24, 25, 
        24, 25, 26, 27, 28, 29, 
        28, 29, 30, 31, 32, 1
    ]

# The expansion function
def expansion(Rn):
    # Rn is a 32-bit binary string
    expanded = ''.join([Rn[i - 1] for i in E])
    return expanded

# S-box Table
Sboxes = [
        
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],

        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],

        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],

        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],

        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],

        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

# P-Box permutation table
P = [
        16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
    ]

# S-box substitution
def substitution(xor_result):
    # The xor_result is the expansion[R(i-1)] XOR Ki
    # Break into 8 blocks of 6 bits each (for the 8 S-boxes)
    blocks = [xor_result[i:i + 6] for i in range(0, len(xor_result), 6)]
    sbox_result = ''
    
    for i, block in enumerate(blocks):
        # First and last bit for row (2 bits)
        row = int(block[0] + block[5], 2)
        # Middle 4 bits for column
        col = int(block[1:5], 2)
        # Substitute with the corresponding S-box
        sbox_value = Sboxes[i][row][col]
        # Convert to 4-bit binary and append
        sbox_result += f'{sbox_value:04b}'
        
    return sbox_result # 4 * 8 = 32 bits long


# Permutation using P-box
def permutation(sbox_output):
    return ''.join([sbox_output[i - 1] for i in P])

# F-function
def F(Rn, Kn):
    # 1. Expansion
    expanded_Rn = expansion(Rn)
    # 2. XOR with the round key
    xor_result = bin(int(expanded_Rn, 2) ^ int(Kn, 2))[2:].zfill(48)
    # 3. Substitution using S-boxes
    substituted = substitution(xor_result)
    # 4. Permutation using P-box
    permuted = permutation(substituted)
    return permuted # Permuted is the desired output F(Ri-1,Ki)


## Add code here :


'''
======================== PHASE IV ========================
'''


# Final Permutation Table
FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]


# 16 DES rounds
def des_encrypt(L0, R0, ActualKMAP):
    # Loop over 16 rounds
    for i in range(1, 17):  # 16 rounds, keys are indexed from 1 to 16 in ActualKMAP
        
        # L(n) = R(n-1)
        Ln = R0 
        
        # R(n) = L(n-1) ^ F(R(n-1), Kn)
        Rn = bin(int(L0, 2) ^ int(F(R0, ActualKMAP[i]), 2))[2:].zfill(32)  
        
        # Prepare for next round
        L0 = Ln
        R0 = Rn
        
        print(f"Round {i}: L{i} = {L0}, R{i} = {R0}\n")
    
    # After the 16th round, combine L16 and R16
    combined = R0 + L0  # R16 + L16 (Swapping the sides for the final permutation)
    return combined

# Final permutation
def final_permutation(combined):
    return ''.join([combined[i - 1] for i in FP])

# Encrypt the message with the given key
def des(K, M):
    # Convert K and M to binary (64-bit representations)
    KB = bin(K)[2:].zfill(64)
    MB = bin(M)[2:].zfill(64)

    # Step 1: Apply the initial permutation on the message (M)
    PM = "".join([MB[x - 1] for x in IP])  # Initial Permutation
    L0, R0 = PM[:32], PM[32:]  # Split into L0 and R0 (32-bits each)

    # Step 2: Generate the 16 keys
    ActualKMAP = {
        round_num: ''.join(KB[i - 1] for i in PC2)
        for round_num, KB in KMAP.items()
    }

    # Step 3: Apply the 16 DES rounds
    combined = des_encrypt(L0, R0, ActualKMAP)

    # Step 4: Apply the final permutation
    ciphertext = final_permutation(combined)
    return ciphertext

'''
======================== PHASE V ========================
'''
# Testing the encryption

# Define the key and message (64 bits each)
K = 0x0f1571c947d9e859  # 64-bit key
M = 0x02468aceeca86420  # 64-bit message

# Encrypt the message using DES
ciphertext = des(K, M)

# Print the final ciphertext in hexadecimal form
print(f"Ciphertext: {hex(int(ciphertext, 2))[2:].upper()}")




