# Text Processing, search for and manipulate text based on patterns
# Regular Expression uses a search pattern to find a string or set of strings
import re

# Check Password Strength Function
def check_password_strength(password):
    """Evaluates the strength of a given password."""

    # Using score to keep track of the password strength
    score = 0
    # Give feedback to the user password whether it strong or not
    feedback = []

    # Criteria 1: Length of Password
    if len(password) >= 12:
        score += 2 # Add 2 to the score
        feedback.append("Good Length.") # Provide the feedback
    elif len(password) >= 8:
        score += 1
        feedback.append("Acceptable length, try making it longer.")
    else:
        feedback.append("Password is too short, minimum of 8 characters is recommended.")
    
    # Criteria 2: Uppercase Letters
    # re.search() tries to find any occurrence of an uppercase letter within the password string
    if re.search(r"[A-Z]", password): # Match any single character from A to Z
        score += 1 # Add 1 to the score
        feedback.append("Contains uppercase letters.") # Provide the feedback
    else:
        feedback.append("Consider adding some uppercase letters.")

    # Criteria 3: Lowercase Letters
    if re.search(r"[a-z]", password):
        score += 1 # Add 1 to the score
        feedback.append("Contains lowercase letters.") # Provide the feedback
    else:
        feedback.append("Consider adding some lowercase letters.")
    
    # Criteria 4: Digits
    if re.search(r"\d", password):
        score += 1 # Add 1 to the score
        feedback.append("Contains digits in the password .") # Provide the feedback
    else:
        feedback.append("Consider adding some digits.")
    
    # Criteria 5: Special Character
    if re.search(r"[!@#$%^&*()_+\-=[\]{}|;':\",.<>/?`~]", password):
        score += 1 # Add 1 to the score
        feedback.append("Contains special characters.") # Provide the feedback
    else:
        feedback.append("Consider adding some special characters.")
    
    # Criteria 6: Avoid common patterns
    if any(common_pattern in password.lower() for common_pattern in ["password", "123456", "qwerty"]):      
        score -= 2 # Deduct 2 points for common patterns
        feedback.append("Avoid common and easily guessed patterns.") # Provide the feedback

    # Print the Strength Report
    print("\n--- Password Strength Report ---")
    # Hash the password
    print(f"Your password {'*' * len(password)}") 
    # Score out of 7
    print(f"Overall Score: {score}/6 (Higher is better)")

    # Score is 6
    if score == 6:
        print("Strength: VERY STRONG")
    # Score is 5 or 4
    elif score >= 4:
        print("Strength: STRONG")
    # Score is 3 or 2
    elif score >= 2:
        print("Strength: MEDIUM")
    # Anything lower than 2
    else:
        print("Strength: WEAK")

    # Print the feedback of each criteria
    print("\nFeedback:")
    for item in feedback:
        print(f"-{item}")

# Main Function
def main():
    # While loop, ask user for their password
    while True:
        password = input("\Enter a password to check (or 'quit' to exit): ")
        # Check if they typed quit (QUIT -> quit)
        if password.lower() == 'quit':
            break
        # Call Function
        check_password_strength(password)

# Entry Point for the Script
if __name__ == "__main__":
    main()