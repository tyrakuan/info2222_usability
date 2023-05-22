from imports import render_template

# Database stores entry within a dict: the username is the key and the value is the class instance when a user registers
class Database:    
    
    def __init__(self):
        self.dict_database = {}
        self.course_guide_table = [
            {"week": "1", "topic": "Introduction and overview", "assignments": ""},
            {"week": "2", "topic": "Cryptography basics I", "assignments": ""},
            # Add more initial table rows here
        ]
        self.course_guide_paragraph_content = """
        This unit provides an integrated treatment of two critical topics for a computing professional:
        human computer interaction (HCI) and security. The techniques and core ideas of HCI will be
        studied with a particular focus on examples and case studies related to security. This unit
        builds the students' awareness of the deep challenges in creating computing systems that can
        meet people's needs for both HCI and security. It will develop basic skills to evaluate systems
        for their effectiveness in meeting people's needs within the contexts of their use, building
        knowledge of common mistakes in systems, and approaches to avoid those mistakes.
    """
        
    def add_entry(self, data):
        # data -> (username, password, salt, role)
        new_user = User(data)
        
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
    
    def update_course_guide(self, paragraph):
        # self.course_guide_table = table
        self.course_guide_paragraph_content = paragraph


# Class instance for every user
class User:
    def __init__(self, data):
        self.username = data[0]
        self.password = data[1]
        self.salt = data[2]
        self.role = data[3]
        