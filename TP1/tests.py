from classes import *

def testLab1_part1():
  monGroupe = Group("ZpAdditive", 0, 23, 23)
  print("In Z23 : exp(5,7) = 12 ?", monGroupe.exp(5,7) == 12)
  Z23_mult = Group("ZpMultiplicative", 1, 22, 23)
  print("In (Z23)* : exp(5,7) = 17 ?", Z23_mult.exp(5,7) == 17)
  print("In Z23 : exp(5,-1) = 18 ?", monGroupe.exp(5,-1) == 18)
  print("In (Z23)* : exp(5,-1) = 14 ?", Z23_mult.exp(5,-1) == 14)
  #Test de DLbyTrialMultiplication
  sub_Z809 = SubGroup("ZpAdditive", 0, 809, 809, 3)
  i = 500
  h = sub_Z809.exp(sub_Z809.g, i)
  print("In the subgroup of Z809 : i = ", sub_Z809.DLbyTrialMultiplication(h))
  
  sub_Z809_mult = SubGroup("ZpMultiplicative", 1, 808, 809, 3)
  i = 500
  h = sub_Z809_mult.exp(sub_Z809_mult.g, i)
  print("In the subgroup of (Z809)* : i = ", sub_Z809_mult.DLbyTrialMultiplication(h))
  
testLab1_part1()