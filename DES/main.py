'''
======================== PHASE I ========================
'''

K = 0x0f1571c947d9e859
M = 0x02468aceeca86420  # Message is one block (64 bits long)

# Convert K and M to Binary representation (64 bits)
KB = bin(K)[2:].zfill(64)
MB = bin(M)[2:].zfill(64)

# Permutation Choice 1 (PC1)
PC1 = [
    57, 49, 41, 33, 25, 17, 9,  1, 58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4
]  # 56-bit key after permutation

# Apply PC1 to get a 56-bit key (K_)
K_ = ''.join([KB[x-1] for x in PC1])

# Split K_ into C0 and D0 (28 bits each)
C0, D0 = K_[:28], K_[-28:]

'''
======================== PHASE II ========================
'''

def left_shift(bits, num_shifts):
    """Perform a circular left shift on a bit string."""
    return bits[num_shifts:] + bits[:num_shifts]

def apply_key_shifts(C0, D0):
    """Generates 16 subkeys for the DES algorithm after applying shifts."""
    KMAP = {}
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    for i in range(16):
        C0 = left_shift(C0, shift_table[i])
        D0 = left_shift(D0, shift_table[i])
        KMAP[i+1] = C0 + D0  # Combine Cn and Dn to create subkeys
    
    return KMAP

KMAP = apply_key_shifts(C0, D0)

# Permutation Choice 2 (PC2) to reduce subkeys to 48 bits
PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

# Generate actual 48-bit subkeys using PC2
ActualKMAP = {
    round_num: ''.join(KMAP[round_num][i - 1] for i in PC2)
    for round_num in KMAP
}

'''
======================== PHASE III ========================
'''

# Initial Permutation (IP) Table
IP = [ 
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

def initial_permutation(MB):
    """Apply initial permutation on the message."""
    return ''.join([MB[i-1] for i in IP])

def expansion(Rn):
    """Expansion function: expand 32-bit Rn to 48-bit."""
    E = [
        32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
    ]
    return ''.join([Rn[i-1] for i in E])

def substitution(xor_result):
    """Apply S-box substitution."""
    # Define all S-boxes
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
    
    # Split the XOR result into 8 blocks of 6 bits
    blocks = [xor_result[i:i+6] for i in range(0, len(xor_result), 6)]
    sbox_result = ''
    
    for i, block in enumerate(blocks):
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        sbox_result += f'{Sboxes[i][row][col]:04b}'
    
    return sbox_result

def permutation(sbox_output):
    """Apply the P-box permutation."""
    P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    return ''.join([sbox_output[i - 1] for i in P])

def F(Rn, Kn):
    """The F-function used in each DES round."""
    expanded_Rn = expansion(Rn)
    xor_result = bin(int(expanded_Rn, 2) ^ int(Kn, 2))[2:].zfill(48)
    substituted = substitution(xor_result)
    return permutation(substituted)

'''
======================== PHASE IV ========================
'''

# Final Permutation Table (FP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]

def final_permutation(combined):
    """Apply final permutation on the combined L and R."""
    return ''.join([combined[i-1] for i in FP])

def des_encrypt(L0, R0, ActualKMAP):
    """Apply 16 DES rounds to the message."""
    for i in range(1, 17):
        Ln = R0
        Rn = bin(int(L0, 2) ^ int(F(R0, ActualKMAP[i]), 2))[2:].zfill(32)
        L0, R0 = Ln, Rn
        print(f"Round {i}: L{i} = {L0}, R{i} = {R0}")
    return R0 + L0  # Return combined result after 16 rounds (R16 + L16)


def des(K, M):
    
    """Main DES encryption function."""
    PM = initial_permutation(MB)
    L0, R0 = PM[:32], PM[32:]

    combined = des_encrypt(L0, R0, ActualKMAP)
    
    final_result = final_permutation(combined)
    
    # Convert binary result to hex and return
    return hex(int(final_result, 2))[2:].upper()


'''
======================== EXECUTION ========================
'''

# Encrypt using the DES function
encrypted_message = des(K, M)
print("Encrypted message:", encrypted_message)


