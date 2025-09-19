from classes import *

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


testLab1_part1()
testLab1_part2()
testLab1_part5()
testLab2_part1()
testLab2_part2()