# Class instance for every message
class MessageDatabase:

    msg_counter = 0 # increment key
    
    def __init__(self):
        self.msg_database = {}

    def add_message_to_database(self, data):

        # data -> (key, username, title, message)
        message = Message(data)
        message.key = self.msg_counter

        self.msg_database.update({message.key: message})

        self.msg_counter += 1


    def read_from_database(self):

        f = open("msg.txt", "w")

        for k, v in self.msg_database:
            print(k, v[1], v[2], v[3])
            f.writelines(k, v[1], v[2], v[3])

        f.close()


class Message:
    def __init__(self, data):
        self.key = 0 # this will be updated
        self.username = data.get('username')
        self.title = data.get('title')
        self.message = data.get('message')