
from collections import deque
queue = deque([[0,0,0]])
trees = []

tarX,tarY , num = input().split(" ")
tarX,tarY,num = int(tarX),int(tarY),int(num)


for i in range(num):
    treeCurrent = input().split(" ")
    for i in range(len(treeCurrent)):
        treeCurrent[i] = int(treeCurrent[i])
    trees.append(treeCurrent)

def directions(trees,posX,posY):
    valid = []
  
    if trees[posY][posX+1] == 1 and posX + 1 < num:
        valid.append((1,0))

    if trees[posY][posX-1] == 1 and posX - 1 > 0:
        valid.append((-1,0))

    if trees[posY+1][posX] == 1 and posY + 1 < num:
        valid.append((0,1))

    if trees[posY-1][posX] == 1 and posY - 1 > 0:
        valid.append((0,-1))
    
    return valid

def bfs (queue,tarX,tarY,trees):
    visited = []
    while len(queue) > 0:
        print("queue",queue)
        posX,posY, dist = queue.popleft()
        print("positions:",posX,posY, dist)

        
        for i in directions(trees, posX,posY):
            newX = posX +i[0]
            newY = posY+i[1]
            if newX!= tarX and newY !=tarY and (newX,newY) not in visited:
                visited.append([newX,newY,dist+1])
                print("queue:",queue)
                queue.append([[newX,newY,dist+1]])
                print("after queue:",queue)
            return(posX+i[0],posY+i[-1],dist+1)
    

valid = directions(trees,tarX,tarY)
print("valid:",valid)

print("trees:",trees)
print("bfs:",bfs(queue,tarX,tarY,trees))


'''

2 2 4
1 1 1 1
1 0 0 1
1 1 1 1
1 1 0 1

'''
