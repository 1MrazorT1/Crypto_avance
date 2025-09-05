import math
class Group(object):
  def __init__(self, l, e, N, p):
    self.l = l
    self.e = e
    self.N = N
    self.p = p
    if self.checkParameters() != True:
      raise Exception("Problem with parameters")
  
  def checkParameters(self):
    if self.l == "":
      raise Exception("l is unknown.")
    return (self.l == "ZpAdditive" and self.e == 0) or (self.l == "ZpMultiplicative" and self.e == 1)

  def law(self, g1, g2):
    if self.l == "ZpAdditive":
      return (g1 + g2) % self.p
    else:
      return (g1 * g2) % self.p

  def exp(self, g, k):
    if k == 0:
      return self.e
    elif k == -1:
      return self.exp(g, self.N-1)
    else:
      h0 = self.e
      h1 = g
      t = math.floor(math.log2(k))
      for i in range(t, -1, -1):
        ki = (k >> i) & 1
        if ki == 0:
          h1 = self.law(h0, h1)
          h0 = self.law(h0, h0)
        else:
          h0 = self.law(h0, h1)
          h1 = self.law(h1, h1)
      return h0
