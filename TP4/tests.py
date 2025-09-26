from classes import *
from hashlib import sha384
from fonctions import *

def testLab1_part1():
  monGroupe = Group("ZpAdditive", 0, 23, 23)
  print("In Z23 : exp(5,7) = 12 ?", monGroupe.exp(5,7) == 12)
  Z23_mult = Group("ZpMultiplicative", 1, 22, 23)
  print("In (Z23)* : exp(5,7) = 17 ?", Z23_mult.exp(5,7) == 17)
  print("In Z23 : exp(5,-1) = 18 ?", monGroupe.exp(5,-1) == 18)
  print("In (Z23)* : exp(5,-1) = 14 ?", Z23_mult.exp(5,-1) == 14)


  #Test de DLbyTrialMultiplication
  sub_Z809 = SubGroup("ZpAdditive", 0, 809, 809, None, 3)
  i = 500
  h = sub_Z809.exp(sub_Z809.g, i)
  print("In the subgroup of Z809 : i = ", sub_Z809.DLbyTrialMultiplication(h))
  
  sub_Z809_mult = SubGroup("ZpMultiplicative", 1, 808, 809, None, 3)
  i = 500
  h = sub_Z809_mult.exp(sub_Z809_mult.g, i)
  print("In the subgroup of (Z809)* : i = ", sub_Z809_mult.DLbyTrialMultiplication(h))

def testLab1_part2():
  sub_Z809 = SubGroup("ZpAdditive", 0, 22, 23, None, 5)
  print("Test de testDiffieHellman : ", sub_Z809.testDiffieHellman())
  print("Test de DiffieHellman sur sous groupe de Z809 : ", sub_Z809.DiffieHellman(5, 6, 2, 7, 12))

  #Testing the law in F2^n
  F256 = Group("F2^n", 1, 8, 2, 283) #283 = 2^8 + 2^4 + 2^3 + 2^1 + 2^0
  print("In F2^8 : 45 x 72 = 198 ?", F256.law(45, 72) == 198)

  #Verifying that DLbyTrialMultiplication returns the good result
  i = randint(1, 255)
  F256x = SubGroup("F2^n", 1, 8, 2, 283, 3)
  h = F256x.exp(F256x.g, i)
  print("In F2^256, DLbyTrialMultiplication returns the googd result : ", i == F256x.DLbyTrialMultiplication(h))

def testLab1_part5():
  i = randint(1, 255)
  F256x = SubGroup("F2^n", 1, 8, 2, 283, 3)
  h = F256x.exp(F256x.g, i)
  print("In F2^256, DLbyTrialMultiplication returns the googd result : ", i == F256x.ComputeDL(h))

def testLab2_part1():
  p  = 2**256-2**224+2**192+2**96-1
  A  = -3
  B  = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
  N  = int("ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551", 16)
  Gx = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
  Gy = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
  P256 = SubGroup("ECConZp", [0,0], N, p, None, [Gx, Gy], A=A, B=B)
  print("P-256 : verify(G) == True ?", P256.verify([Gx, Gy]) == True)
  print("P-256 : verify(O infinity) == True ?", P256.verify([0,0]) == True)
  print("P-256 : verify((Gx, Gy+1)) == False ?", P256.verify([Gx, (Gy + 1) % p]) == False)

  #Testing the ECDSA public key google's certificates
  GooglePublicKey = open("google.der", 'rb')
  PK = GooglePublicKey.read()
  Pkx = int.from_bytes(PK[0xbf:0xdf], byteorder='big')
  Pky = int.from_bytes(PK[0xdf:0xff], byteorder='big')
  GooglePublicKey.close()
  #print(hex(Pkx), hex(Pky))
  print("Is the point from the ECDSA google's public key in the curve P256 ?", P256.verify([Pkx, Pky]) == True)

  print("In P-256, is test de diffie Hellman == True ?", P256.testDiffieHellman())

def testLab2_part2():
  P256 = SubGroup("ECConZp", [0,0], int("ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551", 16), 2**256-2**224+2**192+2**96-1, None, [int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16), int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)], A=-3, B=int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16))
  m = "Example of ECDSA with P-256"
  sk =int("c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96", 16)
  k = int("7a1a7e52797fc8caaa435d2a4dace39158504bf204fbe19f14dbb427faee50ae", 16)
  t = int("2b42f576d07f4165ff65d1f3b1500f81e44c316f1f0b3ef57325b69aca46104f", 16)
  s = int("dc42c2122d6392cd3e3a993a89502a8198c1886fe69d262c4b329bdb6b63faf1", 16)
  Q = P256.exp(P256.g, sk)

  print("test de ecdsa_verif() : ", [t, s] == P256.ecdsa_sign(m, sk, k))
  print("test de ecdsa_sign() : ",P256.ecdsa_verif(m, P256.ecdsa_sign(m, sk, k), Q))

  AlicePublicKey = open("ecdhkeyAlice.der", 'rb')
  PK = AlicePublicKey.read()
  Sk = int.from_bytes(PK[0x07:0x27], byteorder='big')
  Pkx = int.from_bytes(PK[0x39:0x59], byteorder='big')
  Pky = int.from_bytes(PK[0x59:0x79], byteorder='big')
  AlicePublicKey.close()
  #print(hex(Pkx), hex(Pky))
  msg = open("Lab2.pdf","rb").read()
  sig = P256.ecdsa_sign(msg, Sk)
  ok = P256.ecdsa_verif(msg, sig, [Pkx,Pky])
  print("Signature valid?", ok)

def testLab3_part1():
  wikipedia_key = open("wikipedia.der", 'rb')
  c = wikipedia_key.read()
  cert_without_sig = c[0x04:0x04 + 1513]
  hashed_d = sha384(cert_without_sig).digest()
  hashed_h = sha384(cert_without_sig).hexdigest()
  correct_hash = "01c61c9f693846678ce029fa62663baed9cee2618f04df6321bc0bcd2ef867594d99303a374ea9dd36a088742789d40a"
  print("Is the hashed certificate without signature correct ?", hashed_h == correct_hash)
  
  t = int.from_bytes(c[0x600 : 0x600 + 48], byteorder='big')
  s = int.from_bytes(c[0x633 : 0x633 + 49], byteorder='big')
  wikipedia_key.close()
  PK = "04D9F19E4687F8217160A826EBA3FAB9EADA1DB912A7D426D95114B1617C7596BF220B391FD5BED10A46AA2D3C4A09842EBE409555E91940376675ED324E770449F8707BC318E7CEF77110FEAC74D800D4ED6D1C731633109C3AB2EA6C62F4BDB8"
  pkx = int(PK[2 : 2 + 96], 16)
  pky = int(PK[2 + 96 : 2 + 96 + 96], 16)
  p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
  n = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
  A = -3
  b = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef
  Gx = 0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7 
  Gy = 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f
  P384 = SubGroup("ECConZp", [0, 0], n, p, None, [Gx, Gy], A, b)
  sig = [t, s]
  ok = P384.ecdsa_verif(hashed_d, sig, [pkx, pky])
  print("Is the signature of the wikipedia certificate valid ?", ok)

def testLab3_part2():
  n = 0x40000000000000000000292fe77e70c12a4234c33
  poly = 2**163 + 2**7 + 2**6 + 2**3 + 1
  Gx = 5759917430716753942228907521556834309477856722486
  Gy = 1216722771297916786238928618659324865903148082417
  A = 1
  B = 2982236234343851336267446656627785008148015875581
  G = [Gx, Gy]
  B163 = SubGroup("ECC_F2^n", None, n, 0, poly, G, A, B)
  print("Is the provided G on the curve B163 ?", B163.verify(G))
  print("Is the testDiffieHellman successful using the curve B163 ?", B163.testDiffieHellman())
  
  msg = "Example of ECDSA with B-163"
  d = 0x348d138c2de9447bd288feed177222ee377fb7bea
  Qx = 0x66b015c0b72b0f81b1ecba6f58e7545d94744644c
  Qy = 0xba6d4d62419155b186a29784f4aa4b8e8e1e7f76
  Q = [Qx, Qy]
  k = 0x8ed0f93f7d492bb3991847d0e96f9cc3947259aa
  sig = B163.ecdsa_sign(msg, d, k)
  print("Are ecdsa_sign() and ecdsa_verif functional and coherent using the curve B163 ?", B163.ecdsa_verif(msg, sig, Q))

  # Verifying the B163 keys
  b163key = open("b163key.der", 'rb')
  PK = b163key.read()
  d = 0x015ee7c3a3d278e32d5243fd52cea520b1b01cea3c
  Qx = 0x0329a5742bc450f9003356b58be07d1abbb3a7aa48
  Qy = 0x0663bad7d7e7ac3b91e937c5a4f85180ad281763f5
  Q  = [Qx, Qy]
  print("Is the public key correctly generated from the private key ?",Q == B163.exp(B163.g, d))
  print("Is the public key on curve B163? ", B163.verify(Q))
  b163key.close()

def testLab3_part3():
  p = 2**255 - 19
  A = 486662
  N = 2**252 + 0x14def9dea2f79cd65812631a5cf5d3ed
  Gx = 9
  Gy = 0x20ae19a1b8a086b4e01edd2c7748d14c923d4d7e6d7c61b229e9c5a27eced3d9
  G = [Gx, Gy]
  e = [0, 1]
  X25519 = SubGroup("X25519", e, N, p, None, G, A, 1)
  print("Is G on the X25519 curve ?", X25519.verify(G))
  print("Is the inverse of G on the X25519 curve ?", X25519.verify([Gx, -Gy]))
  print("Is the testDiffieHellman true on the curve X25519 ?", X25519.testDiffieHellman())

  #Verifying the Keys of Alice and Bob (second part of Part 3) - I was found at difficulity trying to extract relevant keys with slicing so I had to lean on ChatGPT's help to do so...
  public_key_Alice = open("public_key_Alice.der","rb").read()[-32:]
  public_key_Bob = open("public_key_Bob.der","rb").read()[-32:]
  u_Alice = int.from_bytes(public_key_Alice, "little")
  u_Bob = int.from_bytes(public_key_Bob, "little")
  print("Is the public key of Alice on the X25519 curve (Euler criteria) ?", is_on_X25519_Euler_criteria(u_Alice, p, A))
  print("Is the public key of Alice on the X25519 curve (Euler criteria) ?", is_on_X25519_Euler_criteria(u_Bob, p, A))

  KA = open("key_Alice.der","rb").read()
  iA = KA.rfind(b"\x04\x20")
  key_Alice = KA[iA+2:iA+2+32]
  KB = open("key_Bob.der","rb").read()
  iB = KB.rfind(b"\x04\x20")
  key_Bob = KB[iB+2:iB+2+32]
  print("Does the public key of Alice (resp. Bob) correspond to the multiplication of the private key and G ?", X25519.DiffieHellman(key_Alice, key_Bob, public_key_Alice, public_key_Bob, None))

def test_block_header_extraction():
    block_sample = "010000008095126f08f377b143410cc3c5da3f3d25732d014dc9da1855e8e713000000005a1b723ae6c479056af838a6ea40db6f4acee39f262bf49864cd98f511221d5c7f1ff84b249c151c23af360b0201000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0704249c151c0176ffffffff01c090ec2f01000000434104e1ab3a971f202c86fdd25d8d9f3b486b80bb30ad36d93c030f409918df7f670f6b148400fff9676c70810391b38875ef613987234252cba32d36eae99e05e5a5ac0000000001000000830d2e8f94c33a10f3834554cc1f1469e069f0fcf31a47309d42a9d00f4ba57d86000000008c493046022100bc57dc26f46fecc1da03272cb2298d8a08b22d865541f5b3a3e862cc87da4b47022100ce1fc72771d164d608b15065832542a0e9040cfdf28862c5175c81fcb0e0b65501410434417dd8d89deaf0f6481c2c160d6de0921624ef7b956f38eef9ed4a64e36877be84b77cdee5a8d92b7d93694f89c3011bf1cbdf4fd7d8ca13b58a7bb4ab0804ffffffff1bdfd08a1713d1add2c8624975dbb795de0c7038bca7242d032d0e0b6e92b2a1000000008c49304602210097f8cd3973e5d4c7a2556c82539a710345f82f089398649684a12b3026ae9de5022100d3e46fa2e95988e132f609d267fb403c679a60c3d9d3f936e54f8b4f76d4e4a301410434417dd8d89deaf0f6481c2c160d6de0921"
    block_sample = block_sample[:160]

    block_version = 0x01
    block_id_previous_hash = 0x0000000013e7e85518dac94d012d73253d3fdac5c30c4143b177f3086f129580
    Merkle_root = 0x5c1d2211f598cd6498f42b269fe3ce4a6fdb40eaa638f86a0579c4e63a721b5a
    block_timestamp = 0x4bf81f7f
    field_bits = 0x1c159c24
    nonce = 0xb36af23

    block_version = block_version.to_bytes(4, byteorder='little')
    block_id_previous_hash = block_id_previous_hash.to_bytes(32, byteorder='little')
    Merkle_root = Merkle_root.to_bytes(32, byteorder='little')
    block_timestamp = block_timestamp.to_bytes(4, byteorder='little')
    field_bits = field_bits.to_bytes(4, byteorder='little')
    nonce = nonce.to_bytes(4, byteorder='little')

    block_header = block_version + block_id_previous_hash + Merkle_root + block_timestamp + field_bits + nonce
    block_header = block_header.hex()
    print("Is the data extracted are exactly the 160 first characters of the true block ? ", block_header == block_sample)

def verifying_raw_data():
  with open("block_57043.json", "r") as f:
    data = load(f)
  id_block = list(data["data"].keys())[0]
  block_header = bytes.fromhex(data["data"][id_block]["raw_block"][:160])
  count_hex = data["data"][id_block]["raw_block"][160:162]
  raw_block = bytes.fromhex(data["data"][id_block]["raw_block"])
  mining_transaction = "bd9075d78e65a98fb054cb33cf0ecf14e3e7f8b3150231df8680919a79ac8fe5"
  pizza_transaction = "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"
  concat_hex = block_header + count_hex + mining_transaction_hex + pizza_transaction_hex
  return raw_block == bytes.fromhex(concat_hex)

#testLab1_part1()
#testLab1_part2()
#testLab1_part5()
#testLab2_part1()
#testLab2_part2()
#testLab3_part1()
#testLab3_part2()
#testLab3_part3()
test_block_header_extraction()
checkHeader()
verifying_raw_data()