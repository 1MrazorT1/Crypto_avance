def is_on_X25519_Euler_criteria(u, p, A):
    x = ((u**3 % p) + A * (u**2 % p) + u) % p
    return x == 0 or pow(x, (p - 1) // 2, p) == 1

def reverse_bytes_25519(b):
    return sum(((b >> 8 * (31- i)) & 0xff) << (8*i) for i in range(32))
