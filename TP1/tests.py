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



testLab1_part1()
testLab1_part2()