import sys
import random
import math
import pygame

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
        Maze[ind][i][0] = [ind-1,i]
        Maze[ind-1][i][2] = [ind,i]

        # print(stack)
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
    queue.append([height//2, width//2-1])
    queue.append([height//2, width//2])
    queue.append([height//2-1, width//2])
    queue.append([height//2-1, width//2-1])
    
    
    
    #floodfill
    while queue: #count <= mazeHeight*mazeWidth:
        check = queue.pop()
        for i in range(4):
            if maze[check[0]][check[1]][i] != [None,None] :
                if manhDist[Maze[check[0]][check[1]][i][0]][Maze[check[0]][check[1]][i][1]] == None :
                    manhDist[Maze[check[0]][check[1]][i][0]][Maze[check[0]][check[1]][i][1]] = manhDist[check[0]][check[1]] + 1
                    queue.insert(0, maze[check[0]][check[1]][i])
    return manhDist

#setting display parameters
pygame.init()
cellSize = 40
wallThickness = 4
screen = pygame.display.set_mode((mazeWidth*cellSize+wallThickness,mazeHeight*cellSize+wallThickness))
clock = pygame.time.Clock()

pygame.display.set_caption('Maze generator')

pygame.font.init()
num_font = pygame.font.SysFont('freesansbold', 14)

mazeBoard = make_board(mazeHeight, mazeWidth)
Maze = generate(mazeHeight, mazeWidth)
manhDistGrid = floodfill(Maze, mazeHeight, mazeWidth)



while True:
    screen.fill((80,60,175))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #draw maze
    for i in range(mazeHeight) :
        for j in range(mazeWidth) :
            if Maze[i][j][3] == [None, None] :
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(j*cellSize, i*cellSize, wallThickness, cellSize))
            if Maze[i][j][0] == [None, None] :
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(j*cellSize, i*cellSize, cellSize, wallThickness))
    #draw left over border
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(mazeWidth*cellSize ,0 ,wallThickness, mazeHeight*cellSize))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,mazeHeight*cellSize  ,mazeWidth*cellSize+wallThickness ,wallThickness))

    #write down floodfill numbers
    for i in range(mazeHeight) :
        for j in range(mazeWidth) :
            num_text = num_font.render(str(manhDistGrid[i][j]), True, (0,0,0),(80,60,175))
            num_rect = num_text.get_rect()
            num_rect.topleft = (j*cellSize+3+wallThickness,i*cellSize+3+wallThickness)
            screen.blit(num_text, num_rect)

    pygame.display.update()
    clock.tick(1)
