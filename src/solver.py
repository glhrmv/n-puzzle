import sys
from collections import deque
from bisect import bisect_left, insort
from queue import PriorityQueue, Empty
from copy import deepcopy

# Returns (x, y) coordinates of search in state
def tile_pos(state, search):
	for x, column in enumerate(state):
		for y, tile in enumerate(column):
			if tile == search:
				return x, y

	raise ValueError("tile " + str(search) + " does not exist in state " + str(state))

# Performs an action, which essentially moves the empty space
# in a direction specified by the action taken.
# Returns the new state created.
def _move(state, tile_to_swap):
	x, y = tile_pos(state, '0')
	x2, y2 = x + tile_to_swap[0], y + tile_to_swap[1]
	
	if x2 not in range(len(state)) or y2 not in range(len(state[0])): 
		return None
	
	new_state = deepcopy(state)
	new_state[x][y], new_state[x2][y2] = new_state[x2][y2], new_state[x][y]
	
	return new_state

def up(state):
	return _move(state, (0, -1))

def left(state):
	return _move(state, (-1, 0))

def down(state):
	return _move(state, (0, 1))

def right(state):
	return _move(state, (1, 0))

# (Heuristic 1) Calculate number of misplaced tiles
def misplaced_tiles(current_state, desired_state):
	misplaced = 0

	for x, column in enumerate(current_state):
		for y, tile in enumerate(column):
			if tile != desired_state[x][y]:
				misplaced += 1
	
	return misplaced

# (Heuristic 2) Calculate sum of distances between misplaced
# tiles and their desired position
def manhattan_distance(current_state, desired_state):
	d = 0
	
	for column in current_state:
		for tile in column:
			cur, des = tile_pos(current_state, tile), tile_pos(desired_state, tile)
		d += abs(cur[0] - des[0]) + abs(cur[1] - des[1])
	
	return d
	
class Node(object):
	def __init__(self, state, parent, action_taken):
		self.state = state
		self.parent = parent
		self.action_taken = action_taken
		# Number of nodes from starting node, essentially g(n)
		self.num_parents = 0 if parent == None else parent.num_parents + 1

	# Override < operator, needed for heap
	def __lt__(self, other): return False 

def _bisect_index(collection, value):
	# Locate the insertion point for value in collection to maintain sorted order
	i = bisect_left(collection, value)

	if i != len(collection) and collection[i] == value:
		return i

	return None

def _state_is_valid(state, closed_set):
	return (state != None and _bisect_index(closed_set, state) == None)

def _search(initial_state, desired_state, open_set_get, open_set_add):
	def open_set_add_if_new(successor_state, action_taken):
		if _state_is_valid(successor_state, closed_set):
			open_set_add(Node(successor_state, current_node, action_taken))

	def reconstruct_actions(node):
		actions = []

		while node.action_taken != None:
			actions.append(node.action_taken)
			node = node.parent
		
		return actions

	closed_set = []
	current_node = Node(initial_state, None, None)

	# Repeat this until we find a solution
	while current_node.state != desired_state:
		# Adds state to closed_set while maintaining sorted order
		insort(closed_set, current_node.state)
		
		open_set_add_if_new(up(current_node.state), "up; ")
		open_set_add_if_new(left(current_node.state), "left; ")
		open_set_add_if_new(down(current_node.state), "down; ")
		open_set_add_if_new(right(current_node.state), "right; ")

		try:
			# Expand node according to algorithm chosen
			current_node = open_set_get()
		except (IndexError, Empty):
			# Did not find a solution
			return len(closed_set), None

	return len(closed_set), reconstruct_actions(current_node)

def breadth_first(initial_state, desired_state, heuristic=""):
	open_set = deque() 

	return _search(initial_state, desired_state, 
		open_set_get=open_set.popleft, open_set_add=open_set.append)
	
def greedy_best_first(initial_state, desired_state, heuristic=manhattan_distance):
	def open_set_add(node):
		priority = heuristic(node.state, desired_state)
		open_set.put( (priority, node) )

	def open_set_get():
		_, node = open_set.get_nowait()
		return node

	open_set = PriorityQueue()

	return _search(initial_state, desired_state, open_set_get, open_set_add)
	
def a_star(initial_state, desired_state, heuristic=manhattan_distance):
	def open_set_add(node):
		priority = node.num_parents + heuristic(node.state, desired_state)
		open_set.put( (priority, node) )

	def open_set_get():
		_, node = open_set.get_nowait()
		return node

	open_set = PriorityQueue()

	return _search(initial_state, desired_state, open_set_get, open_set_add)

def solve_with(strategy, heuristic, initial_state, desired_state):
	search_strategies = {
		'BFS': breadth_first,
		'G': greedy_best_first,
		'A*': a_star
	}

	heuristics = {
		'mt': misplaced_tiles,
		'md': manhattan_distance
	}

	if strategy.upper() not in search_strategies:
		print("Search strategy '" + strategy + "' is not a valid option. Available: ")
		for s in search_strategies:
			print(s)
		sys.exit()

	if strategy.upper() == 'BFS':
		return search_strategies[strategy.upper()](initial_state, desired_state)

	if heuristic.lower() not in heuristics:
		print("Heuristic function '" + heuristic + "' is not a valid option. Available: ")
		for h in heuristics:
			print(h)
		sys.exit()

	return search_strategies[strategy.upper()](initial_state, desired_state, heuristics[heuristic.lower()])
