# auth.py

def authenticate(username, password, is_signup=False):
    # Read usernames and passwords from a text file
    with open("user_credentials.txt", "r") as file:
        credentials = [line.strip().split(",") for line in file]

    # Check if the provided username and password match any credentials
    for stored_username, stored_password in credentials:
        if username == stored_username:
            if is_signup:
                # If signing up, return False if the username already exists
                return False
            elif password == stored_password:
                # If signing in, return True if both username and password match
                return True

    if is_signup:
        # If signing up and the username doesn't exist, add new credentials to the file
        with open("user_credentials.txt", "a") as file:
            if credentials:
                file.write("\n")  # Add a newline before appending the new user
            file.write(f"{username},{password}")

    return is_signup  # Return True for sign-up and False for sign-in

