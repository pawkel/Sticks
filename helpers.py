import numpy as np

def mod5(n):
  return np.mod(n, 5)

def extractData(data, player):
  if player == 1: ## first player
    l1,r1,l2,r2 = data
  else:
    l2,r2,l1,r1 = data
  return l1, r1, l2, r2

def rePackData(dataList, player):
  if player == 1:
    return dataList
  else:
    lst  = []
    for x in dataList:
      lst.append([x[2], x[3], x[0], x[1]])
    return lst

def swapHands(data, player):
  # Swap hands! Uno :)
  l1, r1, l2, r2 = extractData(data, player)
  if l1 != r1:
    lst = [[r1,l1, l2,r2]]
  else:
    lst = []
  return rePackData(lst, player)

def fingerTouch(data, player):
  # 'Smack'
  l1, r1, l2, r2 = extractData(data, player)
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
  return rePackData(states, player)

def testFt():
  # Testing 1231 testing
  p = 1
  data = [1,0,2,3]
  print(f'\n Sticker fight {data} for p{p}')
  print(fingerTouch(data, p))
  p = 2 
  print(f'\nSticker fight {data} for p{p}')
  print(fingerTouch(data, p))

def combineActions(data, player):
  # 'bam'
  l, r, optl,optr = extractData(data, player)
  if l+r!=5:
    actions =  [[mod5(l+r),0],[0,mod5(r+l)]]
    if [l, r] in actions:
      actions.remove([l,r])
    if [r, l] in actions:
      actions.remove([r,l])
    states = []
    for a in actions:
      states.append(a+[optl,optr])
    
  else:
    states =  []
  return rePackData(states, player)

def testCombineActions():
  # Testing 1231 testing
  p = 1
  data = [1,0,2,3]
  data2 = [1,2,3,4]
  print(f'Combing actions {data}, p{p}')
  print(combineActions(data, p))
  print(f'Combing actions {data2}, p{p}')
  print(combineActions(data2, p))
  p = 2
  print(f'Combing actions {data}, p{p}')
  print(combineActions(data, p))
  print(f'Combing actions {data2}, p{p}')
  print(combineActions(data2, p))

def decompose(data, player):
  # Mushrooms Bactiria Fungi
  l, r, optl,optr = extractData(data, player)
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
  return rePackData(states, player)

def testDecompose():
  # Testing 1231 testing
  for l in range(0,5):
    for r in range(1, 5):
      print(f'Decomposing {l}, {r}')
      print(decompose(l, r,0,0))

def tests():
  # ssshhhhhdssss Testing 
  # testDecompose()
  testCombineActions()
  testFt()

if __name__=='__main__':
  tests()