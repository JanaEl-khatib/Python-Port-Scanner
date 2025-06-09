# Text Processing, search for and manipulate text based on patterns
# Regular Expression uses a search pattern to find a string or set of strings
import hashlib
import re
import requests

# Check Password Strength Function
def check_password_strength(password):
    """Evaluates the strength of a given password."""
     
    # Hash the password when given:
    print("\n--- Hashing Password ---")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print(f"SHA-256 Hashed Password: {hashed_password}")
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

    print("\n--- Breach Check ---")
    # Call the Function
    check_pwned(password)

# Check Password in Have I Been Pwned API Function
def check_pwned(password):
    """ Check if the password has been exposed in a known data breach."""
    
    # Hash the password using SHA-1 (HIBP (Have I Been Pwned) requires SHA-1)
    sha1pwd = hashlib.sha1(password.encode()).hexdigest().upper()

    # Split the hash into prefix (first 5 characters) and suffix (rest)
    # Allows for anonymity (k-anonymity model)
    prefix, suffix = sha1pwd[:5], sha1pwd[5:]

    # Query the HIBP API with only the prefix
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    # Handle API response errors
    if response.status_code != 200:
        print("Could not reach HIBP API. Try again later.")
        return
    
    # Parse the response
    # Each line contains a has suffix and how many times it appeared in breaches
    hashes = (line.split(':') for line in response.text.splitlines())

    # Check if the suffix of our hashed password is in the results
    for h, count in hashes:
        if h == suffix:
            print(f"This password has been found in {count} data breaches!")
            return # Stop checking if found
    
    # Safe password if suffix is not found
    print("This password has not been found in known data breaches.")

# Main Function
def main():
    # While loop, ask user for their password
    while True:
        password = input("\nEnter a password to check (or 'quit' to exit): ")
        # Check if they typed quit (QUIT -> quit)
        if password.lower() == 'quit':
            break
        # Call Function
        check_password_strength(password)

# Entry Point for the Script
if __name__ == "__main__":
    main()