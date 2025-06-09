# Text Processing, search for and manipulate text based on patterns
# Regular Expression uses a search pattern to find a string or set of strings
import hashlib
import re
import requests
import streamlit as st
import json
from datetime import datetime

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(ellipse at bottom, #0d0d0d 0%, #000000 100%);
        background-attachment: fixed;
        background-size: cover;
        color: white;
    }

    /* Star effect using CSS only */
    .stApp::before {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background: url("https://i.ibb.co/N2b1scFY/360-F-329549476-g-Edf-UOnq-JFOUYizc9-FGQjt-Bqvuat-Ngqt.jpg") repeat;
        background-size: cover;
        opacity: 0.5;
        z-index: 0.5;
    }

    /* Twinkle effect */
    @keyframes twinkle {
        0%, 100% { opacity:0.8; }
        50% { opacity:0.3; }
    }

    /* Float animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .floating-moon {
        position: fixed;
        width: 100px;
        z-index: 0.85;
        opacity: 0.5;
        pointer-events: none;
        animation: 
            float 4s ease-in-out infinite,
            twinkle 5s ease-in-out infinite;
        filter: drop-shadow(0 0 10px white);
    }

    /* Text styling */
    h1, h2, h3, p, .markdown-text-container {
        color: #ffffff;
    }

    input, .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid #888;
    }

    </style>
    <!-- Moon images placed randomly -->
    <img class="floating-moon" src="https://i.ibb.co/RFcsW8n/moon-1400-removebg-preview.png" style="top: 10%; left: 5%;">
    <img class="floating-moon" src="https://i.ibb.co/KxBQ1t1c/photo-1527842891421-42eec6e703ea-removebg-preview.png" style="top: 40%; right: 5%;">
    <img class="floating-moon" src="https://i.ibb.co/KxBQ1t1c/photo-1527842891421-42eec6e703ea-removebg-preview.png" style="top: 10%; right: 30%;">
    <img class="floating-moon" src="https://i.ibb.co/tfqVD4B/Full-Moon2010-removebg-preview.png" style="bottom: 15%; left: 5%;">
    <img class="floating-moon" src="https://i.ibb.co/tfqVD4B/Full-Moon2010-removebg-preview.png" style="top: 15%; right: 5%;">
    <img class="floating-moon" src="https://i.ibb.co/RFcsW8n/moon-1400-removebg-preview.png" style="bottom: 10%; right: 5%;">
    """,
    unsafe_allow_html=True
)


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

    return score, feedback

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
            return f"This password has been found in {count} data breaches!"
    
    # Safe password if suffix is not found
    return "This password has not been found in known data breaches."

# Saving Results to a JSON File
def save_results(password, score, feedback, breach_status):
    """Save the password check results to a local JSON File."""

    # Create a dictionary to hold the results
    result = {
        # Add a timestamp for when this result was generated
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        # Masked password
        "masked_password": "*" * len(password),

        # Store the SHA-256 hash of the password
        "sha-256": hashlib.sha256(password.encode()).hexdigest(),

        # Password strength score
        "score": score,

        # Password feedback
        "feedback": feedback,

        # Breach status from the HIBP API
        "breach_status": breach_status
    }

    try:
        # Try to open and load existing results from results.json
        with open("results.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, start with an empty list
        data = []

    # Append the new result to the list
    data.append(result)

    # Write the updated list back to the JSON File
    with open("results.json", "w") as f:
            json.dump(data, f, indent=4)
    
    # Show a success message in the Streamlit app
    st.success("Results are saved to results.json file")

# Streamlit App
# Title of the web app
st.title("Password Strength Checker")
# Password input field
password = st.text_input("Enter a password to test:", type="password")

# If user types a password
if password:
    st.markdown(" Password Evaluation")
    # Run strength checks
    score, feedback = check_password_strength(password)
    
    # Show masked password and SHA-256 hash
    # Hash the password when given:
    st.write("\n--- Hashing Password ---")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    st.write(f"SHA-256 Hashed Password: {hashed_password}")

    # Print the Strength Report
    st.write("\n--- Password Strength Report ---")
    # Hash the password
    st.write(f"Your password {'*' * len(password)}") 
    # Score out of 7
    st.write(f"Overall Score: {score}/6 (Higher is better)")

    # Score is 6
    if score == 6:
        st.success("Strength: VERY STRONG")
    # Score is 5 or 4
    elif score >= 4:
        st.info("Strength: STRONG")
    # Score is 3 or 2
    elif score >= 2:
        st.warning("Strength: MEDIUM")
    # Anything lower than 2
    else:
        st.error("Strength: WEAK")

    # Print the feedback of each criteria
    st.markdown("\nFeedback:")
    for item in feedback:
        st.write(f"-{item}")

    st.markdown("\n--- Breach Check ---")
    # Call the Function
    result = check_pwned(password)
    st.write(result)

    save_results(password, score, feedback, result)

