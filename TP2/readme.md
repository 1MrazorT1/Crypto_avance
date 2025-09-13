# Lab 2 – Elliptic Curve Cryptography

## Overview

This project is part of the Advanced Cryptography course (3A Informatique, majeure CyberIA).  
It introduces elliptic curve groups over prime fields and their applications to Diffie–Hellman key exchange and the Elliptic Curve Digital Signature Algorithm (ECDSA).

The lab is implemented in Python and covers:

1. Elliptic curves over prime fields (P-256 curve).
2. Implementation of the group law on elliptic curves.
3. Verification of public keys extracted from certificates.
4. Diffie–Hellman key exchange on elliptic curves.
5. ECDSA signature generation and verification, including NIST test vectors.
6. Key generation with OpenSSL and signing/verifying external files.

---

## Files Structure
```bash
.
├── Lab2.pdf
├── classes.py
├── ecdhkeyAlice.der
├── fonctions.py
├── google.der
├── google.pem
├── lab1_utils.py
├── readme.md
└── tests.py
```

- classes.py: Implements Group and SubGroup classes extended for elliptic curves:

    - checkParameters() – validates elliptic curve parameters (A, B, p).
    - law(P, Q) – elliptic curve group law (l = "ECConZp").
    - verify(P) – checks if a point belongs to the curve.
    - exp(P, k) – scalar multiplication (Montgomery ladder).
    - ecdsa_sign(m, sk) – signs a message/file with private key sk.
    - ecdsa_verif(m, sig, Q) – verifies a signature with public key Q.

- tests.py: Contains test functions:

    - testLab2_part1: Tests curve definition, group law, and Diffie–Hellman.

    - testLab2_part2: Tests ECDSA signing/verifying with NIST test vectors. It also tests generated Alice’s keys, signs Lab2.pdf, verifies with public key.

- lab1_utils.py : Implements degree calculations and a displaying function.

- google.pem / google.der: Google’s ECDSA certificate, used to extract and verify the public key.

- ecdhkeyAlice.der: Alice’s keypair generated with OpenSSL (DER format).

- Lab2.pdf: Example file to be signed with Alice’s private key.