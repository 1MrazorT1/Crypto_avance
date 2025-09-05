class Group(object):
  def __init__(self, l, e, N, p):
    self.l = l
    self.e = e
    self.N = N
    self.p = p
    if self.checkParameters() != True:
      raise Exception("Problem with parameters")
