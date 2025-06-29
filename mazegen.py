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

def deapth_first(height, width) :
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
        # print(stack)

    return Maze

#setting display parameters
pygame.init()
cellSize = 20
wallThickness = 2
screen = pygame.display.set_mode((mazeWidth*cellSize+wallThickness,mazeHeight*cellSize+wallThickness))
vWall = pygame.Surface((wallThickness, cellSize))
hWall = pygame.Surface((cellSize, wallThickness))
clock = pygame.time.Clock()

pygame.display.set_caption('Maze generator')

mazeBoard = make_board(mazeHeight, mazeWidth)
Maze = deapth_first(mazeHeight, mazeWidth)
for i in Maze:
    print(i)

while True:
    screen.fill((80,60,175))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for i in range(mazeHeight) :
        for j in range(mazeWidth) :
            if Maze[i][j][3] == [None, None] :
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(j*cellSize, i*cellSize, wallThickness, cellSize))
            if Maze[i][j][0] == [None, None] :
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(j*cellSize, i*cellSize, cellSize, wallThickness))

    pygame.display.update()
    clock.tick(1)
