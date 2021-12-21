# Eight puzzle--Heuristic Algorithm

## Algorithm : 
	Breadth-First Search ( h(n)＝0) 
	A* Algorithm（ Misplaced Tile)
	A* Algorithm（ Manhattan distance）

## Outline :   
	python
	process default eight puzzle or user-entered eight puzzle
	show the number of generated nodes, extended nodes, the target node depth and the computation time

## Test cases:
	
	1 3 2		1 2 3		0 1 2		8 7 1		
	4 8 0		4 8 0		4 5 3		6 0 2
	7 5 6		7 6 5		7 8 6		5 4 3
	
	the following case cannot be solved, and the program evaluates each node before reporting the failure(~100,000)
	
	1 2 3
	4 5 6
	8 7 0

