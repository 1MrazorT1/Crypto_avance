from json import load
from hashlib import sha256
from classes import *

def is_on_X25519_Euler_criteria(u, p, A):
    x = ((u**3 % p) + A * (u**2 % p) + u) % p
    return x == 0 or pow(x, (p - 1) // 2, p) == 1

def reverse_bytes_25519(b):
    return sum(((b >> 8 * (31- i)) & 0xff) << (8*i) for i in range(32))

def reverseBytes(data):
    data = bytearray(data)
    data.reverse()
    return bytes(data)

def recoverData(Filename):
    with open(Filename, "r") as f:
        data = load(f)
    id_block = list(data["data"].keys())[0]
    block_header = bytes.fromhex(data["data"][id_block]["raw_block"][:160])
    return (id_block, block_header)

def checkHeader():
    id_block = recoverData("block_57043.json")[0]
    print("The block's identifier :", id_block)
    block_header = recoverData("block_57043.json")[1]
    l = recoverDataFromHeader(block_header)
    print("Block version: ", l[0])
    print("Identifier of the previous block: ", l[1])
    print("Merkle Root: ", l[2])
    print("Timestamp: ", l[3])
    print("Difficulty of mining: ", l[4])
    print("Nonce: ", l[5])
    print("Is the hash of the block's header with SHA256d = the block's id ?", checkIdBlock(id_block, block_header))
    id1 = bytes.fromhex("bd9075d78e65a98fb054cb33cf0ecf14e3e7f8b3150231df8680919a79ac8fe5")
    id2 = bytes.fromhex("a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d")
    m = bytes.fromhex(l[2][2:])
    print("Does the Merkle root correspond to the hash SHA256d of the two identifiers ?", CheckMerkleTree_57043(m, id1, id2))

def recoverDataFromHeader(header):
    blockVersion = "0x" + reverseBytes(header[:4]).hex()
    idPreviousBlock = "0x" + reverseBytes(header[4: 4 + 32]).hex()
    MerkleRoot = "0x" + reverseBytes(header[4 + 32 : 4 + 32 + 32]).hex()
    timestamp = "0x" + reverseBytes(header[4 + 32 + 32 : 4 + 32 + 32 + 4]).hex()
    bits = "0x" + reverseBytes(header[4 + 32 + 32 + 4 : 4 + 32 + 32 + 4 + 4]).hex()
    nonce = "0x" + reverseBytes(header[4 + 32 + 32 + 4 + 4 : 4 + 32 + 32 + 4 + 4 + 4]).hex()
    return [blockVersion, idPreviousBlock, MerkleRoot, timestamp, bits, nonce]

def checkIdBlock(id, h):
    return reverseBytes(sha256(sha256(h).digest()).digest()).hex() == id

def CheckMerkleTree_57043(Merkle_root, id1, id2):
    return reverseBytes(sha256(sha256(reverseBytes(id1) + reverseBytes(id2)).digest()).digest()) == reverseBytes(Merkle_root)

def checkTransactions():
    l = []
    with open("block_57043.json", "r") as f:
        data = load(f)
    id_block = list(data["data"].keys())[0]
    transactions = data["data"][id_block]["tx"]
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    A = 0
    B = 7
    Px = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    Py = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    E = SubGroup("ECConZp", [0, 0], N, p, A, B, g = (Px, Py))