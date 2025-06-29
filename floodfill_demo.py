import random
import math

mazeHeight = 16
mazeWidth = 16


def make_board(mazeHeight, mazeWidth) :
    maze = []
    for i in range(mazeHeight):
        row = []
        for j in range(mazeWidth):
            row.append([[i-1,j],[i,j+1],[i+1,j],[i,j-1]])
        maze.append(row)
    return maze

def make_emptyMaze(mazeHeight, mazeWidth):
    maze = []
    for i in range(mazeHeight):
        row = []
        for j in range(mazeWidth):
            row.append([[None,None],[None,None],[None,None],[None,None]])

        maze.append(row)
    return maze

def rev_direction(n):
    if n == 0:
        return 2
    if n == 1:
        return 3
    if n == 2:
        return 0
    if n == 3:
        return 1

def is_Boundary(coordinate, height, width) :
    if coordinate[0] == -1 or coordinate[0] == height or coordinate[1] == -1 or coordinate[1] == width :
        return False
    else :
        return True
    
def avl_neighbours(Board, stack, visited, height, width) :
    return [i for i in Board[stack[-1][0]][stack[-1][1]] if i not in visited and is_Boundary(i, height, width)]

def vector_to_lstpos(Vector) :
    return abs(2*Vector[0]+1)-1 + abs(3*Vector[1]-1)-1

def generate(height, width) :
    Board = make_board(height, width)
    Maze = make_emptyMaze(height, width)
    stack = []
    visited = []
    #initialise starting position

    initial = [0,0]
    stack.append(initial)
    visited.append(initial)
    while len(visited) != height*width :
        if avl_neighbours(Board, stack, visited, height, width) :
            next = random.choice(avl_neighbours(Board, stack, visited, height, width))
            dirVector = [next[0]-stack[-1][0], next[1]-stack[-1][1]]
            #linking the two bitches
            Maze[stack[-1][0]][stack[-1][1]][vector_to_lstpos(dirVector)] = next
            Maze[next[0]][next[1]][rev_direction(vector_to_lstpos(dirVector))] = stack[-1]
            stack.append(next)
            visited.append(next)
        else :
            while not avl_neighbours(Board, stack, visited, height, width):
                stack.pop()
    
    #connecting centre 4 blocks
    Maze[height//2 - 1][width//2][3] = [height//2 - 1, width//2 - 1]
    Maze[height//2][width//2 - 1][0] = [height//2 - 1, width//2 - 1]
    Maze[height//2][width//2][0] = [height//2 - 1, width//2]
    Maze[height//2][width//2][3] = [height//2, width//2 - 1]
    #removing a few walls, just because.
    for i in range(height) :
        ind = random.randrange(1,width)
        Maze[i][ind][3] = [i,ind-1]
        Maze[i][ind-1][1] = [i,ind]
    for i in range(width) :
        ind = random.randrange(1,height)
        Maze[ind][i][0] = [ind,i]
        Maze[ind-1][i][2] = [ind,i]
    return Maze



def floodfill(maze, height, width) :
    manhDist = []
    for i in range(height):
        l = []
        for j in range(width):
            l.append(None)
        manhDist.append(l)
    queue = []
    #set goal cell
    manhDist[height//2-1][width//2-1] = 0
    manhDist[height//2][width//2] = 0
    manhDist[height//2-1][width//2] = 0
    manhDist[height//2][width//2-1] = 0
    queue.append([height//2-1, width//2-1])
    queue.append([height//2, width//2-1])
    queue.append([height//2-1, width//2])
    queue.append([height//2, width//2])
    #floodfill
    while queue:
        check = queue.pop()
        for i in range(4):
            if maze[check[0]][check[1]][i] != [None,None] :
                if manhDist[Maze[check[0]][check[1]][i][0]][Maze[check[0]][check[1]][i][1]] == None :
                    manhDist[Maze[check[0]][check[1]][i][0]][Maze[check[0]][check[1]][i][1]] = manhDist[check[0]][check[1]] + 1
                    queue.insert(0, maze[check[0]][check[1]][i])

    return manhDist


mazeBoard = make_board(mazeHeight, mazeWidth)
Maze = generate(mazeHeight, mazeWidth)

manhDistGrid = floodfill(Maze, mazeHeight, mazeWidth)
for i in manhDistGrid :
    print(i)
