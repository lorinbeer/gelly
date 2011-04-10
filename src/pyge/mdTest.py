

from dungeon import MultiDict


h = MultiDict()
h[0] = 'yeah'
h[1] = 'no'
h[0] = 'yeah'
print h
for k,each in h.items():
  print k, each
