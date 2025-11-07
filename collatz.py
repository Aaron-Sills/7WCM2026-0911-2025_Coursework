def collatz(n: int):
    """
    Prints the Collatz sequence for a positive integer n
    using recursion.
    """
    # Ensure n is an integer
    n = int(n)
    
    # Print the current number in the sequence
    print(n)
    
    # Base case: The sequence ends when 1 is reached 
    if n == 1:
        return
        
    # Recursive step
    if n % 2 == 0:
        # n is even 
        collatz(n // 2)
    else:
        # n is odd 
        collatz(3 * n + 1)

# --- Example Usage ---
if __name__ == "__main__":
    while True:
        try:
            num = input("Enter a positive integer (or 'q' to quit): ")
            if num.lower() == 'q':
                break
                
            n_int = int(num)
            if n_int <= 0:
                print("Please enter a POSITIVE integer.")
                continue
                
            print(f"--- Collatz sequence for n={n_int} ---")
            collatz(n_int)
            print("--------------------------------------")
            
        except ValueError:
            print("Invalid input. Please enter an integer.")
