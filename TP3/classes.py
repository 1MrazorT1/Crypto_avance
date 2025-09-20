from math import floor, log2, ceil, sqrt
from random import randint
from lab1_utils import deg
import hashlib

class Group(object):
    def __init__(self, l, e, N, p, poly = None, A = None, B = None):
      self.l = l
      self.e = e
      self.N = N
      self.p = p
      self.poly = poly
      self.A = A
      self.B = B
      if self.poly != None:
        self.m = deg(self.poly)
      if self.checkParameters() != True:
        raise Exception("Problem with parameters")
  
    def checkParameters(self):
      if self.l == "":
        raise Exception("l is unknown.")
      if self.l == "ECConZp":
        if self.A == None or self.B == None:
          return False
        #Insuring that A and B are in Fp
        A = self.A % self.p
        B = self.B % self.p
        return (4 * A**3 + 27 * B**2 != 0)
      if self.l == "ECC_F2^n":
        if self.poly == None or self.A == None or self.B == None:
          return False
        return self.B != 0
      return (self.l == "ZpAdditive" and self.e == 0) or (self.l == "ZpMultiplicative" and self.e == 1) or (self.l == "F2^n" and self.e == 1 and self.poly != None and deg(self.poly) > 0)

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
          if (x & (1 << self.m)) > 0:
            x = x ^ self.poly
          y = y >> 1
        return p
      elif self.l == "ECConZp":
        P = g1
        Q = g2
        if P == self.e:
          return Q
        if Q == self.e:
          return P
        p = self.p
        Px = P[0] % p
        Py = P[1] % p
        Qx = Q[0] % p
        Qy = Q[1] % p
        A = self.A % p
        if Px == Qx and Py != Qy:
          return self.e
        if Px == Qx and Py == Qy and Qy == 0:
          return self.e
        tmp = Group("ZpMultiplicative", 1, self.p-1, self.p)
        if Px == Qx and Py == Qy and Qy != 0:
          lamda = ((3 * Px**2 + A) * tmp.exp((2 * Py) % p, -1)) % p
          x = (lamda**2 - 2 * Px) % p
          return([x, (lamda * (Px - x) - Py) % p])
        if Px != Qx:
          lamda = ((Qy - Py) % p) * tmp.exp((Qx - Px) % p, -1) % p
          x = (lamda**2 - Px - Qx) % p
          return([x, (lamda * (Px - x) - Py) % p])
      elif self.l == "ECC_F2^n":
        P = g1
        Q = g2
        if P == self.e:
          return Q
        elif Q == self.e:
          return P
        p = self.p
        Px = P[0]
        Py = P[1]
        Qx = Q[0]
        Qy = Q[1]
        A = self.A
        m = deg(self.poly)
        tmp = Group("F2^n", 1, (1 << m) - 1, 0, poly=self.poly)
        if Px == Qx and (Py ^ Qy) == Px:
          return self.e
        if Px == Qx and Py == Qy:
          if Px == 0:
            return self.e
          lam = Px ^ tmp.law(Py, tmp.exp(Px, -1))
          x = tmp.law(lam, lam) ^ lam ^ A 
          return [x, tmp.law(lam, (Px ^ x)) ^ x ^ Py ]
        if Px != Qx:
          lam = tmp.law((Py ^ Qy), tmp.exp((Px ^ Qx), -1))
          x = tmp.law(lam, lam) ^ lam ^ Px ^ Qx ^ A
          return [x, tmp.law(lam, (Px ^ x)) ^ x ^ Py]


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
    def __init__(self, l, e, N, p, poly = None, g = None, A = None, B = None):
        Group.__init__(self, l, e, N, p, poly, A, B)
        self.g = g

    def verify(self, P):
      if P == self.e:
        return True
      x = P[0]
      y = P[1]
      if self.l == "ECConZp":
        p = self.p
        x = x % p
        y = y % p
        A = self.A % p
        B = self.B % p
        return (y * y % p) == ((x**3 + A * x + B) % p)
      if self.l == "ECC_F2^n":
        m = deg(self.poly)
        tmp = Group("F2^n", 1, (1<<m) - 1, 0, poly = self.poly)
        return (tmp.law(y, y) ^ tmp.law(x, y)) == (tmp.law(tmp.law(x, x), x) ^ tmp.law(self.A, tmp.law(x, x)) ^ self.B)
  
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

    def DLbyBabyStepGiantStep(self, h):
      w = ceil(sqrt(self.N))
      T = []
      for i in range(0, w + 1):
        T.append(self.exp(self.g, i*w))
      print(T)
      for j in range(0, w + 1):
        x = self.law(h, self.exp(self.exp(self.g, -1), j))
        if x == T[i]:
          return (w * i + j) % self.N
  
    def ComputeDL(self, h, to = 1000):
      if self.N <= to:
        return self.DLbyTrialMultiplication(h)
      else:
        return self.DLbyBabyStepGiantStep(h)
      
    def ecdsa_sign(self, m, Sk, k = None):
      tmp = Group("ZpMultiplicative", 1, self.N-1, self.N)
      e = int.from_bytes(hashlib.sha256(str(m).encode()).digest(), "big")
      e = e % self.N
      if k == None:
        k = randint(1, self.N - 1)
      K = self.exp(self.g, k)
      t = K[0] % self.N
      s = (tmp.exp(k, -1) * (e + (Sk * t) % self.N)) % self.N
      return([t, s])
    
    def ecdsa_verif(self, m, sig, Q):
      t = sig[0]
      s = sig[1]
      e = int.from_bytes(hashlib.sha256(str(m).encode()).digest(), "big")
      e = e % self.N
      tmp = Group("ZpMultiplicative", 1, self.N-1, self.N)
      if t not in range(1, self.N) or s not in range(1, self.N):
        return False
      R = self.law(self.exp(self.g, (e * tmp.exp(s, -1)) % self.N), self.exp(Q, (t * tmp.exp(s, -1)) % self.N))
      return R[0] % self.N == t