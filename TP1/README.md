# Lab 1 - Finite Fields and Cryptography

## Overview

This project is part of the Advanced Cryptography course (3A Informatique, majeure MSI).
It introduces finite groups and finite fields with applications to Diffie-Hellman key exchange and Discrete Logarithm Problems (DLPs).

The lab is implemented in Python and covers:

1. Group and SubGroup operations (additive/multiplicative modulo p).
2. Exponentiation via the Montgomery Ladder.
3. Discrete Logarithms via trial multiplication and Baby-Step Giant-Step.
4. The Diffie-Hellman protocol in finite fields.
5. Binary fields F₂ⁿ, using irreducible polynomials for multiplication.

## Files Structure
```bash
.
├── README.md
├── classes.py
├── fonctions.py
├── lab1_utils.py
└── tests.py
```
- classes.py: Implements Group and SubGroup classes with methods:
    - checkParameters() – validates group definition.
    - law(g1, g2) – group operation.
    - exp(g, k) – exponentiation (Montgomery Ladder).
    - DLbyTrialMultiplication(h) – trial-based discrete log.
    - ComputeDL(h, τ) – hybrid DL solver with Baby-Step Giant-Step.
    - DiffieHellman(...) – implementation of DH protocol.
- tests.py: Contains functions testLab1_part1, testLab1_part2, etc., validating all parts of the lab.
- lab1_utils.py: Implements degree calculations and a displaying function.