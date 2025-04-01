import sys
import heapq
import math

# student details
STUDENT_ID = 'a1884747' # your student ID
DEGREE = 'UG' # or PG if you are in the postgraduate course

def parseMap(filePath):
    with open(filePath, 'r') as f:
        lines = f.readLines()
    rows, cols = map(int, lines[0].split())
    start = tuple(map(int, lines[1].split))
    goal = tuple(map(int, lines[2].split))
    map = []
    for line in lines[3:]:
        map.append([int(i) if i != 'X' else 'X' for i in line.split()])
    return rows, cols, start, goal, map

def getMoves():

def getCost():

def bfs(start, goal, map):
    visited = set()
    queue = [(start, 0, [start])] # (position, cost, path)


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
    
    if path:
        print("path:\n", path)
    else:
        print("path:\nnull\n")

if __name__ == "__main__":
    main()