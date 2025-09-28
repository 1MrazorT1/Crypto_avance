from json import load
from hashlib import sha256
from classes import *
import requests
import hashlib


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

    r = requests.get("https://api.blockchair.com/bitcoin/raw/block/" + id_block)
    block = r.json()["data"][id_block]["raw_block"]
    block_header = bytes.fromhex(block[:160])
    transactions = [block[162:162+268], block[162+268:]]
    return (id_block, block_header, transactions)

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
    m = reverseBytes(bytes.fromhex(l[2][2:]))
    print("Does the Merkle root correspond to the hash SHA256d of the two identifiers ?", CheckMerkleTree_57043(m, id1, id2))
    verifying_raw_data()
    transactions = recoverData("block_57043.json")[2]
    t1 = transactions[0]
    t2 = transactions[1]
    print("Does the first Id correspond to the first transaction ?", checkIdTransaction(id1.hex(), t1))
    print("Does the second Id correspond to the second transaction ?", checkIdTransaction(id2.hex(), t2))
    checkTransactions()

def recoverDataFromHeader(header):
    blockVersion = "0x" + reverseBytes(header[:4]).hex()
    idPreviousBlock = "0x" + reverseBytes(header[4: 4 + 32]).hex()
    MerkleRoot = "0x" + reverseBytes(header[4 + 32 : 4 + 32 + 32]).hex()
    timestamp = "0x" + reverseBytes(header[4 + 32 + 32 : 4 + 32 + 32 + 4]).hex()
    bits = "0x" + reverseBytes(header[4 + 32 + 32 + 4 : 4 + 32 + 32 + 4 + 4]).hex()
    nonce = "0x" + reverseBytes(header[4 + 32 + 32 + 4 + 4 : 4 + 32 + 32 + 4 + 4 + 4]).hex()
    return [blockVersion, idPreviousBlock, MerkleRoot, timestamp, bits, nonce]

def verifying_raw_data():
    with open("block_57043.json", "r") as f:
      data = load(f)
    id_block = list(data["data"].keys())[0]
    raw_block_hex = data["data"][id_block]["raw_block"]
    header_hex = raw_block_hex[:160]
    count_hex  = raw_block_hex[160:162]
    mining_len_hex = 268
    mining_transaction_hex = raw_block_hex[162 : 162 + mining_len_hex]
    pizza_transaction_hex  = raw_block_hex[162 + mining_len_hex : ]
    concat_hex = header_hex + count_hex + mining_transaction_hex + pizza_transaction_hex
    print("Is the raw data of the block 57043 the same as Header || 2 || mining transaction || pizza transaction ?", bytes.fromhex(raw_block_hex) == bytes.fromhex(concat_hex))


def checkIdBlock(id, h):
    return reverseBytes(sha256(sha256(h).digest()).digest()).hex() == id

def CheckMerkleTree_57043(Merkle_root, id1, id2):
    return reverseBytes(sha256(sha256(reverseBytes(id1) + reverseBytes(id2)).digest()).digest()) == reverseBytes(Merkle_root)

def checkIdTransaction(id, transaction):
    raw_bytes = bytes.fromhex(transaction)
    h = sha256(sha256(raw_bytes).digest()).digest()
    transaction_id = reverseBytes(h).hex()
    return(transaction_id == id)

def checkTransactions():
    from classes import SubGroup
    data_57044 = load(open("block_57044.json"))
    id_block = list(data_57044["data"].keys())[0]
    tx2_bytes = bytes.fromhex(data_57044["data"][id_block]["raw_block"][-600:])
    id = "cca7507897abc89628f450e8b1e0c6fca4ec3f7b34cccf55f3f531c659ff4d79"
    print("Is the provided Id corresponding to the extracted transaction ?", checkIdTransaction(id, tx2_bytes.hex()))

    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    A = 0
    B = 7
    Px = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    Py = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    E = SubGroup("ECConZp", [0, 0], N, p, None, (Px, Py), A, B)

    version = tx2_bytes[:4]
    input_count = tx2_bytes[4]
    previous_txid = tx2_bytes[5:37]
    previous_output_index = tx2_bytes[37:41]
    scriptsig_length = tx2_bytes[41]
    scriptsig = tx2_bytes[42:42+scriptsig_length]
    sequence = tx2_bytes[42+scriptsig_length:42+scriptsig_length+4]
    outputs_and_locktime = tx2_bytes[42+scriptsig_length+4:]

    signature_length = scriptsig[0]
    signature_der_plus_hashtype = scriptsig[1:1+signature_length]
    public_key_length = scriptsig[1+signature_length]
    public_key_uncompressed = scriptsig[2+signature_length:2+signature_length+public_key_length]

    der = signature_der_plus_hashtype[:-1]
    r_length = der[3]
    r_value = int.from_bytes(der[4:4+r_length], "big")
    s_length = der[5+r_length]
    s_value = int.from_bytes(der[6+r_length:6+r_length+s_length], "big")

    public_key_x = int.from_bytes(public_key_uncompressed[1:33], "big")
    public_key_y = int.from_bytes(public_key_uncompressed[33:65], "big")
    Q = [public_key_x, public_key_y]
    print("Is Q on secp256k1 ? ", E.verify(Q))

    H = hashlib.new("ripemd160", hashlib.sha256(public_key_uncompressed).digest()).digest()
    pkscript = bytes.fromhex("76a914" + H.hex() + "88ac")
    print("Is pkscript computed from the public key 04 || Qx || Qy ? ", pkscript.hex() == "76a91446af3fb481837fadbb421727f9959c2d32a3682988ac")

    a = version + bytes([input_count]) + previous_txid + previous_output_index + b"\x19" + pkscript + sequence + outputs_and_locktime + b"\x01\x00\x00\x00"
    z = hashlib.sha256(hashlib.sha256(a).digest()).digest()
    print("Is the hash value equal to the one given in the lab ?", z.hex() == "c2d48f45d7fbeff644ddb72b0f60df6c275f0943444d7df8cc851b3d55782669")
    print("Is the signature valid ? ", E.ecdsa_verif(z, [r_value, s_value], Q))


#I have relied on the assistance of AI for the understanding of this part...
def build_jer_basecheck_address():
    data_57044 = load(open("block_57044.json", "r"))
    id_block = list(data_57044["data"].keys())[0]
    tx2_bytes = bytes.fromhex(data_57044["data"][id_block]["raw_block"][-600:])

    scriptsig_length = tx2_bytes[41]
    scriptsig = tx2_bytes[42:42+scriptsig_length]
    signature_length = scriptsig[0]
    public_key_length = scriptsig[1+signature_length]
    public_key_uncompressed = scriptsig[2+signature_length:2+signature_length+public_key_length]

    public_key_hash160 = hashlib.new("ripemd160", hashlib.sha256(public_key_uncompressed).digest()).digest()
    payload = b"\x00" + public_key_hash160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address_bytes = payload + checksum

    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(address_bytes, "big")
    address_base58 = ""
    while n > 0:
        n, rest = divmod(n, 58)
        address_base58 = alphabet[rest] + address_base58
    leading_zero_bytes = 0
    for byte in address_bytes:
        if byte == 0:
            leading_zero_bytes += 1
        else:
            break
    address = "1" * leading_zero_bytes + address_base58

    print("Is the H given for debug correct ? ", public_key_hash160.hex() == "46af3fb481837fadbb421727f9959c2d32a36829")
    print("Are the bytes correct ? ", checksum.hex() == "71c823e7")
    print("Does the address found correspond to the identifier of Jeremy Sturdivant ?", address == "17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ")
