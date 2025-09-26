from json import load

def is_on_X25519_Euler_criteria(u, p, A):
    x = ((u**3 % p) + A * (u**2 % p) + u) % p
    return x == 0 or pow(x, (p - 1) // 2, p) == 1

def reverse_bytes_25519(b):
    return sum(((b >> 8 * (31- i)) & 0xff) << (8*i) for i in range(32))

def reverseBytes(data):
    data = bytearray(data)
    data.reverse()
    return data

def recoverData(Filename):
    with open(Filename, "r") as f:
        data = load(f)
    id_block = list(data["data"].keys())[0]
    block_header = data["data"][id_block]["raw_block"][:160]
    return block_header

def checkHeader():
    print()

