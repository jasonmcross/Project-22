
from userDB import DatabaseOperations

if __name__ == "__main__":
    db = DatabaseOperations()

    # Add a user
    db.add_user("example@example.com", "John", "password123")
    # Show a user
    user = db.lookup_user_info("example@example.com")
    if user:
        print("User found:", user)
    else:
        print("User not found.")

    # Remove a user
    db.remove_user("example@example.com")

    # Show a user (after removal)
    user = db.lookup_user_info("example@example.com")
    if user:
        print("User found:", user)
    else:
        print("User not found.")