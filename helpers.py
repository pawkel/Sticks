import numpy as np

def mod5(n):
  return np.mod(n, 5)
  
def swapHands(l1,r1, l2, r2):
  # Swap hands! Uno :)
  if l1 != r1:
    return [r1,l1, l2,r2]
  else:
    return []

def fingerTouch(l1,r1, l2,r2):
  # 'Smack'
  states = []
  if l1!=0:
    if l2!=0:
      states.append([l1,r1,mod5(l1+l2), r2])
    if r2!=0:
      states.append([l1,r1,l2, mod5(l1+r2)]) 
  if r1!=0:
    if l2!=0:
      states.append([l1,r1,mod5(r1+l2), r2])
    if r2!=0:
      states.append([l1,r1,l2, mod5(r1+r2)]) 
  return states

def testFt():
  # Testing 1231 testing
  for i in range(0, 5):
    for j in range(0, 5):
      # for i2 in range(0, 5):
      #   for j2 in range(0,5):
        i2, j2 = 1, 2
        print(f'\ntesting {i,j,i2,j2}')
        print(fingerTouch(i,j,i2,j2))

def combineActions(l,r, optl, optr):
  # 'bam'
  if l+r!=5:
    actions =  [[mod5(l+r),0],[0,mod5(r+l)]]
    if [l, r] in actions:
      actions.remove([l,r])
    if [r, l] in actions:
      actions.remove([r,l])
    states = []
    for a in actions:
      states.append(a+[optl,optr])
    return states
  else:
    return []

def testCombineActions():
  # Testing 1231 testing
  for l in range(0,5):
    for r in range(1, 5):
      print(f'Combing actions {l}, {r}')
      print(combineActions(l, r, 0, 0) )

def decompose(l, r, optl,optr):
  # Mushrooms Bactiria Fungi
  N = l+r
  combos = []
  for i in range(N+1):
    lr = [mod5(i),mod5(N-i)]
    if lr in [[0,0],[l,r], [r,l],[r+l, 0],
    [0,r+l],[mod5(l+r),0],[0,mod5(l+r)]]:
      continue
    if not (lr in combos):
      combos.append(lr)
  states = []
  for a in combos:
    states.append(a+[optl,optr])
  return states

def testDecompose():
  # Testing 1231 testing
  for l in range(0,5):
    for r in range(1, 5):
      print(f'Decomposing {l}, {r}')
      print(decompose(l, r,0,0))

def tests():
  # ssshhhhhdssss Testing 
  # testDecompose()
  # testCombineActions()
  testFt()

if __name__=='__main__':
  tests()