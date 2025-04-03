import sys
import heapq
import math

# student details
STUDENT_ID = 'a1884747' # your student ID
DEGREE = 'UG' # or PG if you are in the postgraduate course

def parseMap(filePath):
    with open(filePath, 'r') as f:
        lines = f.readlines()
    row, col = map(int, lines[0].split()) 
    start = (int(lines[1].split()[0]) - 1, int(lines[1].split()[1]) - 1)
    goal = (int(lines[2].split()[0]) - 1, int(lines[2].split()[1]) - 1)
    grid = [] # [(line1), (line2), (line3), ...]
    for line in lines[3:]:
        grid.append([int(i) if i != 'X' else 'X' for i in line.split()])
    return row, col, start, goal, grid

def getMoves(x, y, grid):
    row, col = len(grid), len(grid[0])
    formula = [(1,0), (-1,0), (0,1), (0,-1)]
    moves = []

    for nx, ny in formula:
        nx, ny = nx + x, ny + y
        if 0 <= nx < row and 0 <= ny < col and grid[nx][ny] != 'X':
            moves.append((nx,ny))
    return moves

def getCost(curr, next):
    elevation = next - curr
    if elevation > 0:
        return 1 + elevation
    else:
        return 1
         
def bfs(start, goal, grid):
    visited = set()
    queue = [(start, [start])] # (position, path)
    while queue:
        (row,col), path = queue.pop(0)
        if (row,col) == goal:
            return path
        if (row,col) in visited:
            continue
        visited.add((row,col))
        for nx,ny in getMoves(row, col, grid):
            queue.append(((nx,ny), path + [(nx,ny)]))
    return None

def ucs(start, goal, grid):
    visited = {}
    priorityQ = [(0, start, [start])] # (cost, position, path)
    while priorityQ:
        cost, (row,col), path = heapq.heappop(priorityQ)
        if (row,col) == goal:
            return path
        if (row,col) in visited and visited[(row,col)] <= cost:
            continue
        visited[(row,col)] = cost
        for nx,ny in getMoves(row, col, grid):
            newCost = cost + getCost(grid[row][col], grid[nx][ny])
            heapq.heappush(priorityQ, (newCost, (nx,ny), path + [(nx,ny)]))
    return None

def heuristic(curr, goal, heur):
    x1, y1 = curr
    x2, y2 = goal
    if heur == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    elif heur == "euclidean":
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return 0

def astar(start, goal, grid, heur):
    
    visited = set()
    priorityQ = [(0, start, [start])] # (cost, position, path)
    costsG = {start: 0}

    while priorityQ:
        cost, (row,col), path = heapq.heappop(priorityQ)

        if (row,col) == goal:
            return path
        
        if (row,col) in visited:
            continue
        visited.add((row,col))

        for nx,ny in getMoves(row, col, grid):
            fG = costsG[(row,col)] + getCost(grid[row][col], grid[nx][ny])
            fH = heuristic((nx,ny), goal, heur)
            fF = fG + fH

            if (nx,ny) not in costsG or fG < costsG[(nx,ny)]:
                costsG[(nx,ny)] = fG
                heapq.heappush(priorityQ, (fF, (nx,ny), path + [(nx,ny)]))

    return None

def main():
    mode = sys.argv[1]
    mapFile = sys.argv[2]
    algorithm = sys.argv[3]
    heuristic = sys.argv[4] if len(sys.argv) > 4 else None
    rows, cols, start, goal, grid = parseMap(mapFile)

    if algorithm == "bfs":
        path = bfs(start, goal, grid)
    elif algorithm == "ucs":
        path = ucs(start, goal, grid)
    elif algorithm == "astar":
        path = astar(start, goal, grid, heuristic)
    else:
        print("invalid, choose bfs, ucs, or astar")
        sys.exit(1)

    if path:
        #path 
        print("path:")
        pathGrid = [[str(cell) for cell in row] for row in grid]
        for r, c in path:
            pathGrid[r][c] = '*'
        for row in pathGrid:
            print(" ".join(row))
        #visits

    else:
        print("path:\nnull\n")

if __name__ == "__main__":
    main()