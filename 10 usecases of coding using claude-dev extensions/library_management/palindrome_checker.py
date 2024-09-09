def is_palindrome(s: str) -> bool:
    """
    Check if a given string is a palindrome.
    
    This function ignores case sensitivity and spaces. It returns True if
    the string is a palindrome and False otherwise.
    
    Args:
        s (str): The input string to check.
    
    Returns:
        bool: True if the string is a palindrome, False otherwise.
    
    Example:
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("race a car")
        False
    """
    # Remove spaces and convert to lowercase
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    # Check if the cleaned string is equal to its reverse
    return cleaned == cleaned[::-1]


# Test the function
if __name__ == "__main__":
    test_cases = [
        "A man a plan a canal Panama",
        "race a car",
        "Was it a car or a cat I saw?",
        "Hello, World!",
        "",  # Empty string
        "a",  # Single character
        "aba",  # Odd length palindrome
        "abba",  # Even length palindrome
    ]
    
    for test in test_cases:
        result = is_palindrome(test)
        print(f"'{test}' is {'' if result else 'not '}a palindrome.")