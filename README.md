# Password Strength Checker

This project is a simple **command-line tool** that evaluates the strength of a user-entered password using **regular expressions (regex)** and basic rules of good password hygiene. It provides feedback and a score based on various security criteria.

---

## Features

- Evaluates passwords based on:
  - Length
  - Use of uppercase and lowercase letters
  - Inclusion of digits
  - Inclusion of special characters
  - Avoidance of common insecure patterns (e.g. "password", "123456")
- Provides clear feedback on how to improve weak passwords
- Assigns an overall score from 0 to 6
- Categorizes strength as: **WEAK**, **MEDIUM**, **STRONG**, or **VERY STRONG**

---

## How It Works

The script uses Python's built-in `re` module to scan the password for:
- Character types using regex patterns
- Insecure patterns like `"password"` or `"123456"`

The score is determined based on how many of the 6 checks your password passes.

---

## Example Usage

```bash
$ python password_checker.py

Enter a password to check (or 'quit' to exit): 

--- Password Strength Report ---
Your password ************
Overall Score: 6/6 (Higher is better)
Strength: VERY STRONG

Feedback:
- Good Length.
- Contains uppercase letters.
- Contains lowercase letters.
- Contains digits in the password.
- Contains special characters.
