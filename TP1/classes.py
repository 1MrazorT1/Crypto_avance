from math import floor, log2, ceil, sqrt
from random import randint
from lab1_utils import deg

class Group(object):
  def __init__(self, l, e, N, p, poly = None):
    self.l = l
    self.e = e
    self.N = N
    self.p = p
    self.poly = poly
    if self.poly != None:
      self.N = deg(self.poly)
    if self.checkParameters() != True:
      raise Exception("Problem with parameters")
  
  def checkParameters(self):
    if self.l == "":
      raise Exception("l is unknown.")
    return (self.l == "ZpAdditive" and self.e == 0) or (self.l == "ZpMultiplicative" and self.e == 1) or (self.l == "F2^n" and self.e == 1 and self.poly != None and deg(self.poly) == self.N)

  def law(self, g1, g2):
    if self.l == "ZpAdditive":
      return (g1 + g2) % self.p
    elif self.l == "ZpMultiplicative":
      return (g1 * g2) % self.p
    elif self.l == "F2^n":
      p = 0
      x = g1
      y = g2
      while y != 0:
        if (y & 1) > 0:
          p = p ^ x
        x = x << 1
        if (x & (1 << self.N)) > 0:
          x = x ^ self.poly
        y = y >> 1
      return p

  def exp(self, g, k):
    if k == 0:
      return self.e
    elif k == -1:
      return self.exp(g, self.N-1)
    else:
      h0 = self.e
      h1 = g
      t = floor(log2(k))
      for i in range(t, -1, -1):
        ki = (k >> i) & 1
        if ki == 0:
          h1 = self.law(h0, h1)
          h0 = self.law(h0, h0)
        else:
          h0 = self.law(h0, h1)
          h1 = self.law(h1, h1)
      return h0

class SubGroup(Group):
  def __init__(self, l, e, N, p, poly, g):
    Group.__init__(self, l, e, N, p, poly)
    self.g = g
  
  def DLbyTrialMultiplication(self, h):
    tmp = self.e
    for i in range((1 << self.N) - 1):
      if tmp == h:
        return i
      else:
        tmp = self.law(tmp, self.g)
  
  def testDiffieHellman(self):
    a = randint(0, self.N)
    b = randint(0, self.N)
    A = self.exp(self.g, a)
    B = self.exp(self.g, b)
    return self.exp(A, b) == self.exp(B, a)
  
  def DiffieHellman(self, a, b, A, B, K):
    return A == self.exp(self.g, a) and B == self.exp(self.g, b) and K == self.exp(A, b) and K == self.exp(B, a)






  
  #def DLbyTrialMultiplication(self, h):
  #  w = ceil(sqrt(self.N))
  #  T = []
  #  for i in range(0, w + 1):
  #    T.append(self.exp(self.g, i*w))
  #  print(T)
  #  for j in range(0, w + 1):
  #    x = self.law(h, self.exp(self.exp(self.g, -1), j))
  #    if x == T[i]:
  #      return (w * i + j) % N
