from json import load
from hashlib import sha256

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
    print("Does the Merkle root correspond to the hash SHA256d of the two identifiers ?", CheckMerkleTree_57043(l[2], id1, id2))

def recoverDataFromHeader(header):
    blockVersion = header[:4]
    idPreviousBlock = header[4: 4 + 32]
    MerkleRoot = header[4 + 32 : 4 + 32 + 32]
    timestamp = header[4 + 32 + 32 : 4 + 32 + 32 + 4]
    bits = header[4 + 32 + 32 + 4 : 4 + 32 + 32 + 4 + 4]
    nonce = header[4 + 32 + 32 + 4 + 4 : 4 + 32 + 32 + 4 + 4 + 4]
    return [blockVersion, idPreviousBlock, MerkleRoot, timestamp, bits, nonce]

def checkIdBlock(id, h):
    return sha256(sha256(h).digest()).hexdigest() == reverseBytes(id.encode())

def CheckMerkleTree_57043(Merkle_root, id1, id2):
    return sha256(sha256(id1 + id2).digest()).hexdigest() == reverseBytes(Merkle_root)