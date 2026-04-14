
def login(username, password):
    if username == "admin" and password == "1234":
        return "Login successful"
    return "Invalid credentials"

def logout():
    return "User logged out"
