import sys
from os import path
import time

from solver import solve_with

def parse_args():
	if len(sys.argv) > 4:
		print("usage: " + sys.argv[0] + " <filename> <search_strategy> [<heuristic>]")
		sys.exit()
	
	filename, search_strategy = sys.argv[1], sys.argv[2]
	heuristic = "none"
	if len(sys.argv) == 4:
		heuristic = sys.argv[3]

	return filename, search_strategy, heuristic

# Converts a single line of a puzzle file that represents a state into an array
def state_from_line(line, width, height):
		state = [[] for x in range(width)]
		
		for x in range(width):
			for y in range(height):
				state[x].append(line[x + y * width])

		return state

def puzzle_from_file(filename):
	if not path.isfile(filename):
		print("file does not exit")
		sys.exit()
	
	with open(filename) as file:
		contents = file.read().split('\n')
		
		dimensions = contents[0].split('x')
		width, height = int(dimensions[0]), int(dimensions[1])

		initial_state = state_from_line(contents[1].split(' '), width, height)
		desired_state = state_from_line(contents[2].split(' '), width, height)

		return initial_state, desired_state

def _main():
	# Get puzzle details
	filename, search_strategy, heuristic = parse_args()
	initial_state, desired_state = puzzle_from_file(filename)
	
	# Start measuring time
	start_time = time.process_time()

	# Call solver
	number_of_nodes, solution = solve_with(search_strategy, heuristic, initial_state, desired_state)
	
	# Print solution details
	print("time taken: " + str(round(time.process_time() - start_time, 5)) + " secs")
	print("file: " + filename)
	print("strategy: " + search_strategy.upper() + " (heuristic: " + heuristic.lower() + ")")
	print("nodes followed: " + str(number_of_nodes))
	print("solution:")

	# Print actions taken
	if solution == None:
		print("no solution found.")
	else:
		for action in reversed(solution): 
			print(action, end='')
		print("")

if __name__ == "__main__":
	_main()
