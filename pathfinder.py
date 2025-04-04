import sys
import heapq
import math
#
# student details
STUDENT_ID = 'a1884747' # your student ID
DEGREE = 'UG' # or PG if you are in the postgraduate course
#
# parsing sys input
def parseMap(filePath):
    with open(filePath, 'r') as f:
        lines = f.readlines()
    row, col = map(int, lines[0].split()) 
    start = (int(lines[1].split()[0]) - 1, int(lines[1].split()[1]) - 1)
    goal = (int(lines[2].split()[0]) - 1, int(lines[2].split()[1]) - 1)
    grid = [] 
    for line in lines[3:]:
        grid.append([int(i) if i != 'X' else 'X' for i in line.split()])
    return row, col, start, goal, grid
#
# getting move and cost
def getMoves(x, y, grid):
    row, col = len(grid), len(grid[0])
    formula = [(-1,0), (1,0), (0,-1), (0,1)]
    moves = []

    for dx, dy in formula:
        nx, ny = dx + x, dy + y
        if 0 <= nx < row and 0 <= ny < col and grid[nx][ny] != 'X':
            moves.append((nx,ny))
    return moves
#
def getCost(curr, next):
    elevation = next - curr
    if elevation > 0:
        return 1 + elevation
    else:
        return 1
#
# getting basic grids for outputs
def getVisitsGrid(grid):
    row = len(grid)
    col = len(grid[0]) if row > 0 else 0
    visits = []
    for r in range(row):
        rVisits = []
        for c in range(col):
            if grid[r][c] == 'X':
                rVisits.append(-1)
            else:
                rVisits.append(0)
        visits.append(rVisits)
    return visits
#
def getFirstVisitsGrid(grid):
    row = len(grid)
    col = len(grid[0]) if row > 0 else 0
    visits = [[None for _ in range(col)] for _ in range(row)]
    for r in range(row):
        for c in range(col):
            if grid[r][c] == 'X':
                visits[r][c] = 'X'
    visits[0][0] = 1
    return visits
#
# getting heuristic
def heuristic(curr, goal, heur):
    x1, y1 = curr
    x2, y2 = goal
    if heur == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    elif heur == "euclidean":
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return 0
#
# search algorithms  
def bfs(start, goal, grid):
    
    visited = set()
    queue = [(start, [start])] 
    allVisits = getVisitsGrid(grid)
    firstVisit = getFirstVisitsGrid(grid)
    lastVisit = getFirstVisitsGrid(grid)
    visitCounter = 1

    while queue:
        (row,col), path = queue.pop(0)

        allVisits[row][col] += 1
        if firstVisit[row][col] is None:
                firstVisit[row][col] = visitCounter
        lastVisit[row][col] = visitCounter
        visitCounter += 1

        if (row,col) == goal:
            return path, allVisits, firstVisit, lastVisit
        if (row,col) in visited:
            continue
        visited.add((row,col))

        for nx,ny in getMoves(row, col, grid):
            queue.append(((nx,ny), path + [(nx,ny)]))
      
    return None, None, None, None
#
def ucs(start, goal, grid):
    visited = {}
    priorityQ = [(0, 1, start, [start])]
    allVisits = getVisitsGrid(grid)
    firstVisit = getFirstVisitsGrid(grid)
    lastVisit = getFirstVisitsGrid(grid)
    visitCounter = 1
    qCounter = 2

    while priorityQ:
        cost, counter, (row,col), path = heapq.heappop(priorityQ)

        allVisits[row][col] += 1
        if firstVisit[row][col] is None:
                firstVisit[row][col] = visitCounter
        lastVisit[row][col] = visitCounter
        visitCounter += 1

        if (row,col) == goal:
            return path, allVisits, firstVisit, lastVisit
        if (row,col) in visited and visited[(row,col)] <= cost:
            continue
        visited[(row,col)] = cost

        for nx,ny in getMoves(row, col, grid):
            newCost = cost + getCost(grid[row][col], grid[nx][ny])
            heapq.heappush(priorityQ, (newCost, qCounter, (nx,ny), path + [(nx,ny)]))
            qCounter += 1

    return None, None, None, None
#
def astar(start, goal, grid, heur):
    
    visited = set()
    priorityQ = [(0, 1, start, [start])] 
    costsG = {start: 0}
    allVisits = getVisitsGrid(grid)
    firstVisit = getFirstVisitsGrid(grid)
    lastVisit = getFirstVisitsGrid(grid)
    visitCounter = 1
    qCounter = 2

    while priorityQ:

        cost, counter, (row,col), path = heapq.heappop(priorityQ)
        
        allVisits[row][col] += 1
        if firstVisit[row][col] is None:
            firstVisit[row][col] = visitCounter
        lastVisit[row][col] = visitCounter
        visitCounter += 1

        if (row,col) == goal:
            return path, allVisits, firstVisit, lastVisit

        if (row,col) in visited:
            continue
        visited.add((row,col))

        for nx,ny in getMoves(row, col, grid):
            fG = costsG[(row,col)] + getCost(grid[row][col], grid[nx][ny])
            fH = heuristic((nx,ny), goal, heur)
            fF = fG + fH
            if (nx,ny) not in costsG or fG < costsG[(nx,ny)]:
                costsG[(nx,ny)] = fG
                heapq.heappush(priorityQ, (fF, qCounter, (nx,ny), path + [(nx,ny)]))
            qCounter += 1

    return None, None, None, None
#
#
def main():
    mode = sys.argv[1]
    mapFile = sys.argv[2]
    algorithm = sys.argv[3]
    heuristic = sys.argv[4] if len(sys.argv) > 4 else None
    rows, cols, start, goal, grid = parseMap(mapFile)

    if algorithm == "bfs":
        path, allVisits, firstVisit, lastVisit = bfs(start, goal, grid)
    elif algorithm == "ucs":
        path, allVisits, firstVisit, lastVisit = ucs(start, goal, grid)
    elif algorithm == "astar":
        path, allVisits, firstVisit, lastVisit = astar(start, goal, grid, heuristic)
    else:
        print("invalid, choose bfs, ucs, or astar")
        sys.exit(1)

    if path:
        if mode == "debug":
            #path 
            print("path:")
            pathGrid = [[str(cell) for cell in row] for row in grid]
            for r, c in path:
                pathGrid[r][c] = '*'
            for row in pathGrid:
                print(" ".join(row))

            #allVisits
            print("#visits:")
            for r in range(rows):
                print(" ".join(
                    'X' if allVisits[r][c] == -1 else ('.' if allVisits[r][c] == 0 else str(allVisits[r][c]))
                    for c in range(cols)
                ))

            # first visit
            print("first visit:")
            for r in range(rows):
                print(" ".join(
                    '.' if firstVisit[r][c] is None else str(firstVisit[r][c]) for c in range(cols)
                ))
            
            #last visit
            print("last visit:")
            for r in range(rows):
                print(" ".join(
                    '.' if lastVisit[r][c] is None else str(lastVisit[r][c]) for c in range(cols)
                ))
        elif mode == "release":
            pathGrid = [[str(cell) for cell in row] for row in grid]
            for r, c in path:
                pathGrid[r][c] = '*'
            for row in pathGrid:
                print(" ".join(row))

    else:
        if mode == "debug": 
            print("path:\nnull\n#visits:\n...\nfirst visit:\n...\nlast visit:\n...\n")
        elif mode == "release":
            print("null")
#
if __name__ == "__main__":
    main()