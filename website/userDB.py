# # import os
# # import psycopg2
# # from dotenv import load_dotenv

# # class DatabaseOperations:
# #     def __init__(self):
# #         load_dotenv()
# #         self.connection_string = os.getenv('DATABASE_URL')
# #         self.conn = psycopg2.connect(self.connection_string)
# #         self.cur = self.conn.cursor()

# #     def __del__(self):
# #         self.cur.close()
# #         self.conn.close()


# #     def add_user(self, email, name, password):
# #         sql = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)"
# #         self.cur.execute(sql, (email, name, password))
# #         self.conn.commit()

# #     def remove_user(self, email):
# #         sql = "DELETE FROM users WHERE email = %s"
# #         self.cur.execute(sql, (email,))
# #         self.conn.commit()

# #     def edit_user_password(self, email, new_password):
# #         sql = "UPDATE users SET password = %s WHERE email = %s"
# #         self.cur.execute(sql, (new_password, email))
# #         self.conn.commit()

# #     def lookup_user(self, email):
# #         sql = "SELECT password FROM users WHERE email = %s"
# #         self.cur.execute(sql, (email,))
# #         return self.cur.fetchone()

# # if __name__ == "__main__":
# #     db = DatabaseOperations()

# #     # Get user input for email
# #     email = input("Enter email: ")

# #     # Lookup user and display password
# #     user_password = db.lookup_user(email)
# #     if user_password:
# #         print("Password:", user_password[0])
# #     else:
# #         print("User not found")





# import os
# import psycopg2
# from dotenv import load_dotenv

# class DatabaseOperations:
#     def __init__(self):
#         load_dotenv()
#         self.connection_string = os.getenv('DATABASE_URL')
#         self.conn = psycopg2.connect(self.connection_string)

#     # def __del__(self):
#     #     self.conn.close()
        
#     def __del__(self):
#      if hasattr(self, 'conn') and self.conn is not None:
#         self.conn.close()


#     def add_user(self, email, name, password):
#         cur = self.conn.cursor()
#         sql = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)"
#         cur.execute(sql, (email, name, password))
#         self.conn.commit()
#         cur.close()

#     def remove_user(self, email):
#         cur = self.conn.cursor()
#         sql = "DELETE FROM users WHERE email = %s"
#         cur.execute(sql, (email,))
#         self.conn.commit()
#         cur.close()

#     def edit_user_password(self, email, new_password):
#         cur = self.conn.cursor()
#         sql = "UPDATE users SET password = %s WHERE email = %s"
#         cur.execute(sql, (new_password, email))
#         self.conn.commit()
#         cur.close()

#     def lookup_user(self, email):
#         cur = self.conn.cursor()
#         sql = "SELECT password FROM users WHERE email = %s"
#         cur.execute(sql, (email,))
#         result = cur.fetchone()
#         cur.close()
#         return result

# # if __name__ == "__main__":
# #     db = DatabaseOperations()

# #     # Get user input for email
# #     email = input("Enter email: ")

# #     # Lookup user and display password
# #     user_password = db.lookup_user(email)
# #     if user_password:
# #         print("Password:", user_password[0])
# #     else:
# #         print("User not found")
