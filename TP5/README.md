# TP5 — Side-Channel Attacks (SPA & CPA)

## Overview

This TP introduces power analysis techniques used to extract cryptographic secrets from physical implementations.
I implemented both the SPA and CPA attacks.

The objectives were:

Part 1 — SPA: recover a private scalar from double-and-add traces (CryptoHack “Double and Broken” challenge).

Part 2 — CPA: recover a key from 50 power traces using the Hamming-weight leakage model.

## File Structure

```bash
.
├── CPA_attack
│   ├── cpa_attack.py
│   ├── data_Lab5
│   │   ├── plaintext.npy
│   │   ├── sbox_aes.py
│   │   └── traces.npy
│   └── trace0.png
├── README.md
└── SPA_attack
    ├── collected_data.txt
    ├── source_snippet.py
    └── spa_attack.py
```

## Files content

- CPA_attack/cpa_attack.py: Implementation of the CPA attack:

Loads traces and plaintexts.

Uses the Hamming-weight model on the S-box output for each byte (1 to 16).

Computes the Pearson correlation between predicted leakages and measured traces.

Compares the recovered key to the actual solution.

- CPA_attack/data_Lab5/

    - plaintext.npy

    - traces.npy

    - sbox_aes.py: S-box definition.

- SPA_attack/source_snippet.py: Provided CryptoHack snippet for Double and Broken on secp256k1.

- SPA_attack/collected_data.txt: 50 recorded traces.

- SPA_attack/spa_attack.py: Implementation of the SPA attack: reconstructs the private key from the 50 repeated multiplications.