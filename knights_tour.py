import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Define the 8 possible moves for a knight
# (x, y) coordinates relative to the current position
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

# Board size (standard 8x8)
N = 8

def create_empty_board():
    """Creates an empty 8x8 board, initialised with zeros."""
    # Using list of lists as requested
    return [[0 for _ in range(N)] for _ in range(N)]

def is_valid_move(board, x, y):
    """Checks if a square (x, y) is valid and unvisited."""
    return 0 <= x < N and 0 <= y < N and board[x][y] == 0

def is_closed_tour(board, x, y, start_x, start_y):
    """Checks if the last move (x, y) can jump back to the start."""
    for move_x, move_y in KNIGHT_MOVES:
        if x + move_x == start_x and y + move_y == start_y:
            return True
    return False

def solve_backtracking_util(board, curr_x, curr_y, move_count, start_x, start_y):
    """
    Recursive utility function for the Backtracking algorithm.
    This implements the rationale for choosing a direction and backtracking.
    """
    board[curr_x][curr_y] = move_count # Mark the square with the move number
    
    # If the tour is complete (all 64 squares visited)
    if move_count == N * N:
        # Check if it's a closed tour 
        return is_closed_tour(board, curr_x, curr_y, start_x, start_y)

    # Try all 8 possible next moves
    for move_x, move_y in KNIGHT_MOVES:
        next_x, next_y = curr_x + move_x, curr_y + move_y
        
        if is_valid_move(board, next_x, next_y):
            # Recurse
            if solve_backtracking_util(board, next_x, next_y, move_count + 1, start_x, start_y):
                return True # Solution found

    # Backtrack 
    # If no move leads to a solution, reset the square and return False
    board[curr_x][curr_y] = 0
    return False

def KnightsTourBacktracking(startingPosition: tuple[int, int]) -> tuple[bool, list[list[int]]]:
    """
    Signature function for the Backtracking Knight's Tour.
    """
    board = create_empty_board()
    start_x, start_y = startingPosition
    
    if not (0 <= start_x < N and 0 <= start_y < N):
        print("Error: Starting position is off the board.")
        return False, board

    is_successful = solve_backtracking_util(board, start_x, start_y, 1, start_x, start_y)
    return is_successful, board

def KnightsTourLasVegas(startingPosition: tuple[int, int]) -> tuple[bool, list[list[int]]]:
    """
    Signature function for the Las Vegas Knight's Tour.
    """
    board = create_empty_board()
    start_x, start_y = startingPosition
    
    if not (0 <= start_x < N and 0 <= start_y < N):
        print("Error: Starting position is off the board.")
        return False, board

    curr_x, curr_y = start_x, start_y
    move_count = 1
    board[curr_x][curr_y] = move_count

    while move_count < N * N:
        # Find all valid next moves
        valid_next_moves = []
        for move_x, move_y in KNIGHT_MOVES:
            next_x, next_y = curr_x + move_x, curr_y + move_y
            if is_valid_move(board, next_x, next_y):
                valid_next_moves.append((next_x, next_y))
        
        # End condition: knight runs out of valid moves
        if not valid_next_moves:
            break # Unsuccessful tour

        # Randomness is applied here 
        # Randomly select one of the valid moves
        next_x, next_y = random.choice(valid_next_moves)
        
        curr_x, curr_y = next_x, next_y
        move_count += 1
        board[curr_x][curr_y] = move_count
        
        # Note: The other end condition (stepping on visited square)
        # is handled by is_valid_move, which is used to build valid_next_moves.

    # Check for success
    # Tour is successful if all squares are visited AND it's a closed tour
    is_successful = (move_count == N * N) and is_closed_tour(board, curr_x, curr_y, start_x, start_y)
    
    return is_successful, board

def visualize_board(board: list[list[int]], title: str):
    """
    Visualization function to show all visited squares.
    This also displays the empty board.
    """
    print(f"Displaying: {title}")
    # Use NumPy for easy plotting with Matplotlib 
    board_array = np.array(board)
    
    plt.figure(figsize=(6, 6))
    # 'matshow' is good for matrices
    plt.matshow(board_array, fignum=1, cmap='cividis')
    
    # Add the move numbers (integers) to the cells
    for i in range(N):
        for j in range(N):
            if board_array[i, j] > 0:
                plt.text(j, i, str(board_array[i, j]), 
                         va='center', ha='center', color='white' if board_array[i, j] < 40 else 'black')
            else:
                plt.text(j, i, '0', va='center', ha='center', color='gray')

    plt.title(title)
    plt.xticks(range(N))
    plt.yticks(range(N))
    plt.gca().invert_yaxis() # Puts (0,0) at top-left
    plt.grid(which='major', color='black', linestyle='-', linewidth=2)
    plt.show()

def run_success_rate_test(algorithm_func, num_runs=10000):
    """
    Tests the success rate of a given algorithm over 10,000 runs.
    """
    print(f"Running {num_runs} tests for {algorithm_func.__name__}...")
    successful_runs = 0
    start_time = time.time()
    
    for i in range(num_runs):
        # Pick a random starting position for each run
        start_pos = (random.randint(0, N-1), random.randint(0, N-1))
        
        # Run the algorithm
        was_successful, _ = algorithm_func(start_pos)
        
        if was_successful:
            successful_runs += 1 # Record successful run [cite: 54]
            
    end_time = time.time()
    
    # Calculate success rate
    rate = (successful_runs / num_runs) * 100
    total_time = end_time - start_time
    
    print(f"--- Results for {algorithm_func.__name__} ---")
    print(f"Total runs: {num_runs}")
    print(f"Successful runs: {successful_runs}")
    print(f"Success Rate: {rate:.2f}%")
    print(f"Total time: {total_time:.2f} seconds")
    return rate

def main():
    """
    Main function to manage user input.
    """
    print("Welcome to the Knight's Tour solver.")
    
    # Create and display the empty board 
    visualize_board(create_empty_board(), "Empty 8x8 Board")

    while True:
        print("\nPlease select an approach:")
        print("1: Backtracking")
        print("2: Las Vegas")
        print("3: Run Success Rate Test (10,000 runs)")
        print("4: Exit program") 
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '4':
            print("Exiting.")
            break
            
        if choice not in ('1', '2', '3'):
            # Manage unexpected inputs 
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue

        if choice == '3':
            # Run the success rate test
            run_success_rate_test(KnightsTourBacktracking)
            run_success_rate_test(KnightsTourLasVegas)
            continue
            
        # Get starting position (e.g., "0,0")
        try:
            pos_input = input("Enter starting position (e.g., '0,0'): ")
            x_str, y_str = pos_input.split(',')
            start_pos = (int(x_str), int(y_str))
        except ValueError:
            print("Invalid format. Please use 'x,y' (e.g., '0,0').")
            continue

        board_result = None
        is_successful = False
        algo_name = ""

        if choice == '1':
            # Backtracking 
            algo_name = "Backtracking"
            print("Running Backtracking... (This may take a long time)")
            is_successful, board_result = KnightsTourBacktracking(start_pos)
            
        elif choice == '2':
            # Las Vegas
            algo_name = "Las Vegas"
            print("Running Las Vegas...")
            is_successful, board_result = KnightsTourLasVegas(start_pos)

        # Display the result
        title = f"{algo_name} Tour (Success: {is_successful})"
        print(f"Tour complete. Success: {is_successful}")
        visualize_board(board_result, title)

if __name__ == "__main__":
    main()
