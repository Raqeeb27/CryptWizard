from random import choice, shuffle
import string

def password_gen(min_length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    pwd = []
    has_number = False
    has_special = False

    while len(pwd) < min_length:
        new_char = choice(characters)

        # Ensure the generated character meets the required criteria
        if numbers and new_char in digits:
            has_number = True
        if special_characters and new_char in special:
            has_special = True

        pwd.append(new_char)

    # If the generated password is shorter than the specified length, add missing characters that meet the criteria
    while len(pwd) < min_length:
        new_char = choice(characters)
        if numbers and not has_number and new_char in digits:
            pwd.append(new_char)
            has_number = True
        if special_characters and not has_special and new_char in special:
            pwd.append(new_char)
            has_special = True

    # Shuffle the password to ensure randomness
    shuffle(pwd)

    return ''.join(pwd)