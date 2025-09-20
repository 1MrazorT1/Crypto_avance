# Lab 3 – Elliptic Curves Cryptography

## Overview

This project is part of the **Advanced Cryptography course (3A Informatique, majeure CyberIA)**.  
It extends the work of Lab 2 by introducing more advanced elliptic curve settings:

1. **Certificate analysis & ECDSA (P-384)**  
   - Parse the certificate of *wikipedia.org*.  
   - Extract the certificate body and compute its SHA-384 hash.  
   - Recover signature components *(s, t)* and the public key of the Certificate Authority.  
   - Verify the signature using the P-384 curve parameters from FIPS 186-4.

2. **Elliptic Cryptography on Binary Fields (B-163)**  
   - Implement group law for curves defined over \( F_{2^n} \).  
   - Verify the base point \( G \) and test Diffie–Hellman key exchange.  
   - Implement ECDSA signing and verifying on B-163 using NIST vector tests.  
   - Generate a keypair with OpenSSL, parse DER files, check that \( Q = d \cdot G \), and confirm that the public key lies on the curve.

3. **Curve25519 / X25519**  
   - Implement the group law for the Montgomery curve \( Y^2 = X^3 + AX^2 + X \) over \( F_p \) with \( p = 2^{255} - 19 \), \( A = 486662 \).  
   - Verify the generator point \( G = (9, Gy) \) and its inverse.  
   - Test Diffie–Hellman key exchange with the custom `DiffieHellman()` method.  
   - Generate Alice and Bob’s keypairs using OpenSSL (`x25519`).  
   - Parse private/public keys from DER/PEM files.  
   - Verify public keys with Euler’s criterion and confirm they correspond to the multiplication of the clamped private key and \( G \).  
   - Show that the shared secret derived by Alice and Bob is identical.

---

## Files Structure
```bash
.
├── README.md
├── X25519key1.bin
├── X25519key2.bin
├── b163key.der
├── classes.py
├── fonctions.py
├── keyAlicex25519.pem
├── keyBobx25519.pem
├── key_Alice.der
├── key_Bob.der
├── lab1_utils.py
├── pubkeyAlicex25519.pem
├── pubkeyBobx25519.pem
├── public_key_Alice.der
├── public_key_Bob.der
├── tests.py
├── wikipedia-org.pem
└── wikipedia.der
```

## Files descriptions

### classes.py
Implements the core `Group` and `SubGroup` classes:

- `checkParameters()` – validates parameters for Zp, F2^n, ECConZp, ECC_F2^n, X25519.  
- `law(P, Q)` – group law (addition of points, Montgomery ladder for X25519).  
- `verify(P)` – tests whether a point lies on the curve.  
- `exp(P, k)` – scalar multiplication.  
- `ecdsa_sign(m, sk, k)` – signs message `m` with private key `sk`.  
- `ecdsa_verif(m, sig, Q)` – verifies signature with public key `Q`.  
- `DiffieHellman(...)` – computes/validates shared key.

---

### fonctions.py
Utility functions:

- `reverse_bytes_25519()` – handles reverseness for Curve25519 keys.  
- `is_on_X25519_Euler_criteria(u, p, A)` – Implements the Euler criterion.

---

### lab1_utils.py
Provides polynomial degree computation for binary fields.

---

### tests.py
Implements the different lab exercises:

- `testLab3_part1` – Wikipedia certificate parsing, SHA-384 hashing, signature verification with P-384.  
- `testLab3_part2` – Curve B-163: verify base point, test DH, run ECDSA with NIST vectors, check key generation via OpenSSL.  
- `testLab3_part3` – X25519: verify curve, test generator inverse, run Diffie–Hellman, parse Alice/Bob keys from DER, confirm Euler criterion and correctness of \( Q = d \cdot G \), check shared secrets.

---

### wikipedia.der
Certificate of *wikipedia.org* in DER format (converted with OpenSSL).

### b163key.der
ECDSA keypair generated for curve B-163 (DER format).

### key_Alice.der / key_Bob.der / public_key_Alice.der / public_key_Bob.der
Alice’s and Bob’s X25519 private/public keys generated with OpenSSL.

### Lab3.pdf
Lab instructions / reference document.