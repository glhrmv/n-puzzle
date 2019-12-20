# n-puzzle

An [n-puzzle](https://en.wikipedia.org/wiki/15_puzzle) solver.

## Usage

With Python3 installed, run the solver with 
```
python3 src/main.py <puzzle file> <strategy> [<heuristic>]
```
where `puzzle file` is a text file specifying a puzzle and
`strategy` is one of the currently supported search strategies. 
The format of a puzzle file must follow a particular structure. 
Example file:
```
2x3          # width x height
1 2 3 4 0 5  # initial state
3 1 2 4 5 0  # desired state
```
There are already some example puzzle files included with the project,
located in the [`puzzles/`](./puzzles/) directory. An example use of the
solver could be `python3 src/main.py puzzles/puzzle1.txt A*`.

The optional argument `heuristic` is one of the currently supported
heuristic functions for the intelligent search algorithms to use. 

## Search strategies

This is the list of currently supported search strategies,
in human-readable form followed by how they must be sent to the program.

Uninformed search algorithms:
- Breadth-first search (`BFS`)

Informed search algorithms:
- Greedy search (`G`)
- A* search (`A*`)

The informed search algorithms can use one of the following heuristics:

- Heuristic 1 (`mt`) (default): number of **m**isplaced **t**iles, i.e., number of blocks in the
current state which don't share the same position with the corresponding
block in the desired state.
- Heuristic 2 (`md`): sum of the **M**anhattan **d**istance of a misplaced block's position
to its desired position, for every misplaced block.

## Results

The program's successful output follows the following structure:
```
time taken: 0.00167 secs        # Time taken
file: puzzles/puzzle1.text      # File used for puzzle
strategy: A* (heuristic: md)    # Strategy used (incl. heuristic)
nodes followed: 4               # Nodes explored
solution:                       # Sequence of actions taken
left; down; right; right;
```
