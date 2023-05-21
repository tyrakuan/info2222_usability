from imports import render_template

# Database stores entry within a dict: the username is the key and the value is the class instance when a user registers
class Database:    
    
    def __init__(self):
        self.dict_database = {}
        
    def add_entry(self, data):
        # data -> (username, password, salt, role)
        new_user = User(data)

        print(new_user.username, new_user.role)
        
        self.dict_database.update({new_user.username: new_user})
        
    def check_database(self, username):
        return self.dict_database.get(username)
    
    def add_to_database(self, data): # checks if entry is in database, if so return error, else add to database - route to login
        if self.check_database(data[0]) is not None:
            print("Already in database")
            return render_template('register.html', return_message="Username already taken")
        
        self.add_entry(data)
        
        return render_template('login.html')
    
    def check_credentials(self, data): # Checks that the username and corresponding password (hash) is correct
        if (user_object := self.check_database(data[0])) is None:
            print("Username not in database")
            return (False, "Username does not exist. Register account.")
            # return render_template('login.html', return_message="Username does not exist. Register account")

        if user_object.password != data[1]:
            print("Password is incorrect")
            return (False, "Password is incorrect. Try again.")
            # return render_template('login.html', return_message="Password is incorrect. Try again")
                
        return (True, user_object.username)


# Class instance for every user
class User:
    
    def __init__(self, data):
        self.username = data[0]
        self.password = data[1]
        self.salt = data[2]
        self.role = data[3]
        