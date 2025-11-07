from collections import Counter

def findMostFrequentWord(inputList1: list[str], inputList2: list[str]) -> str:
    """
    Finds the most frequent word in inputList1 that is not present in inputList2.
    Signature:
    """
    # Use a set for efficient O(1) average-case lookup of words to exclude
    exclude_words = set(inputList2)
    
    # Use collections.Counter to get frequencies of all words in inputList1
    word_counts = Counter(inputList1)
    
    most_frequent_word = ""
    max_frequency = 0
    
    # Iterate through the word counts
    for word, frequency in word_counts.items():
        if word not in exclude_words:
            if frequency > max_frequency:
                max_frequency = frequency
                most_frequent_word = word
                
    return most_frequent_word

def findMostFrequentFollower(inputList: list[str], targetWord: str) -> str:
    """
    Finds the most frequent word that follows targetWord in inputList.
    Tie-breaker: prints the one that occurs last in the array.
    Signature:
    """
    followers = []
    
    # Iterate through the list to find all followers
    for i in range(len(inputList) - 1):
        if inputList[i] == targetWord:
            followers.append(inputList[i+1])
            
    if not followers:
        return "" # No followers found
        
    # Count the frequency of each follower
    follower_counts = Counter(followers)
    
    # Find the maximum frequency
    max_freq = max(follower_counts.values())
    
    # Get all words that have this maximum frequency
    candidates = {word for word, freq in follower_counts.items() if freq == max_freq}
    
    # Handle the tie-breaker: "the one that occurs last in the array" 
    # We iterate through our list of followers *in reverse*.
    # The first one we find that is in our set of candidates is the correct answer.
    for follower in reversed(followers):
        if follower in candidates:
            return follower
            
    return "" # Should be unreachable if followers list is not empty

# --- Example Usage ---
if __name__ == "__main__":
    
    # --- Task 3.a ---
    a1 = ["apple", "banana", "apple", "orange", "banana", "apple", "grape"]
    a2 = ["orange", "grape", "pear"]
    
    print("--- Task 3.a: findMostFrequentWord ---")
    print(f"List a1: {a1}")
    print(f"List a2: {a2}")
    most_frequent = findMostFrequentWord(a1, a2)
    print(f"Most frequent word in a1 not in a2: '{most_frequent}'") # Expected: 'apple'
    
    a1_2 = ["a", "b", "c", "a", "c", "c", "b"]
    a2_2 = ["a"]
    print(f"\nList a1: {a1_2}")
    print(f"List a2: {a2_2}")
    most_frequent_2 = findMostFrequentWord(a1_2, a2_2)
    print(f"Most frequent word in a1 not in a2: '{most_frequent_2}'") # Expected: 'c'

    # --- Task 3.b ---
    # Example from prompt 
    a1_text = "This is the way. The way is shut. The door is the end."
    # We need to process this string into a list of strings
    a1_list = a1_text.replace('.', '').split()
    
    print("\n--- Task 3.b: findMostFrequentFollower ---")
    print(f"Input List: {a1_list}")
    
    # Example 1
    target1 = "the"
    follower1 = findMostFrequentFollower(a1_list, target1)
    print(f"Target: '{target1}'. Follower: '{follower1}'") # Expected: 'way'
    
    # Example 2 
    target2 = "is"
    follower2 = findMostFrequentFollower(a1_list, target2)
    print(f"Target: '{target2}'. Follower: '{follower2}'") # Expected: 'the'
    
    # Example 3
    target3 = "door"
    follower3 = findMostFrequentFollower(a1_list, target3)
    print(f"Target: '{target3}'. Follower: '{follower3}'") # Expected: 'is'
    
    # Tie-breaker example
    a1_tie = ["a", "b", "a", "c", "a", "b"]
    target_tie = "a"
    # Followers: ["b", "c", "b"]
    # Counts: {"b": 2, "c": 1}
    # Result: "b"
    print(f"\nInput List: {a1_tie}")
    follower_tie_1 = findMostFrequentFollower(a1_tie, target_tie)
    print(f"Target: '{target_tie}'. Follower: '{follower_tie_1}'") # Expected: 'b'
    
    a1_tie_2 = ["a", "b", "a", "c"]
    # Followers: ["b", "c"]
    # Counts: {"b": 1, "c": 1}
    # Tie-breaker: "c" occurs last
    print(f"\nInput List: {a1_tie_2}")
    follower_tie_2 = findMostFrequentFollower(a1_tie_2, target_tie)
    print(f"Target: '{target_tie}'. Follower: '{follower_tie_2}'") # Expected: 'c'
