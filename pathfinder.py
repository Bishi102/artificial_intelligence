import sys
import heapq
import math

# student details
STUDENT_ID = 'a1884747' # your student ID
DEGREE = 'UG' # or PG if you are in the postgraduate course

def parseMap(filePath):
    with open(filePath, 'r') as f:
        lines = f.readLines()
    row, col = map(int, lines[0].split()) 
    start = tuple(map(int, lines[1].split)) # (row,col)
    goal = tuple(map(int, lines[2].split)) # (row,col)
    map = [] # [(line1), (line2), (line3), ...]
    for line in lines[3:]:
        map.append([int(i) if i != 'X' else 'X' for i in line.split()])
    return row, col, start, goal, map

def getMoves(x, y, map):
    row, col = len(map), len(map[0])
    formula = [(1,0), (-1,0), (0,1), (0,-1)]
    moves = []

    for nx, ny in formula:
        nx, ny = nx + x, ny + y
        if 0 <= nx < row and 0 <= ny < col and map[nx][ny] != 'X':
            moves.append((nx,ny))

def getCost(curr, next):
    elevation = next - curr
    if elevation > 0:
        return 1 + elevation
    else:
        return 1
         
def bfs(start, goal, map):
    visited = set()
    queue = [(start, 0, [start])] # (position, path)
    while queue:
        (row,col), path = queue.pop(0)
        if (row,col) == goal:
            return path
        if (row,col) in visited:
            continue
        visited.add((row,col))
        for nx,ny in getMoves(row, col, map):
            queue.append((nx,ny), path + [(nx,ny)])
    return None

# EDIT THIS
def ucs(start, goal, map):
    visited = set()
    queue = [(start, 0, [start])] # (position, path)
    while queue:
        (row,col), path = queue.pop(0)
        if (row,col) == goal:
            return path
        if (row,col) in visited:
            continue
        visited.add((row,col))
        for nx,ny in getMoves(row, col, map):
            queue.append((nx,ny), path + [(nx,ny)])
    return None

# EDIT THIS
def astar(start, goal, map):
    visited = set()
    queue = [(start, 0, [start])] # (position, path)
    while queue:
        (row,col), path = queue.pop(0)
        if (row,col) == goal:
            return path
        if (row,col) in visited:
            continue
        visited.add((row,col))
        for nx,ny in getMoves(row, col, map):
            queue.append((nx,ny), path + [(nx,ny)])
    return None

def main():
    mode = sys.argv[1]
    mapFile = sys.argv[2]
    algorithm = sys.argv[3]
    heuristic = sys.argv[4]
    rows, cols, start, goal, map = parseMap(mapFile)

    if algorithm == "bfs":
        path = bfs()
    elif algorithm == "ucs":
        path = ucs()
    elif algorithm == "astar":
        path = astar()
    else:
        print("invalid, choose bfs, ucs, or astar")
        sys.exit(1)
    
    # EDIT THIS
    if path:
        print("path:\n", path)
    else:
        print("path:\nnull\n")

if __name__ == "__main__":
    main()