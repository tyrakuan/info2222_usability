import json

# Class instance for every message
class MessageDatabase:

    msg_counter = 0 # increment key
    
    def __init__(self):
        self.msg_database = {}

    def add_message_to_database(self, data):

        # data -> (key, username, message)
        data.key = self.msg_counter

        self.msg_database[data.key] = data

        self.msg_counter += 1

    def get_messages(self):
        return self.msg_database


class Message:
    def __init__(self, username, message):
        self.key = 0 # this will be updated
        self.username = username
        self.message = message

    def to_dict(self):
        return {
            'key': self.key,
            'username': self.username,
            'message': self.message,
        }