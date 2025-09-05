from classes import Group

def testLab1_part1():
  monGroupe = Group("ZpAdditive", 0, 23, 23)
  print("In Z23 : exp(5,7) = 12 ?", monGroupe.exp(5,7) == 12)
  Z23_mult = Group("ZpMultiplicative", 1, 22, 23)
  print("In (Z23)* : exp(5,7) = 17 ?", Z23_mult.exp(5,7) == 17)
  print("In Z23 : exp(5,-1) = 18 ?", monGroupe.exp(5,-1) == 18)
  print("In (Z23)* : exp(5,-1) = 14 ?", Z23_mult.exp(5,-1) == 14)

testLab1_part1()