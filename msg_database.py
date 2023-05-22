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

    # def write_to_msg_json(self):
    #     message_dict_json = {k: v.to_dict() for k, v in self.msg_database.items()}

    #     with open("messages.json", "w") as f:
    #         messages_json = json.dumps(message_dict_json)

    #     self.msg_json_file = messages_json # dict to json


    # def get_msg_json(self):
    #     with open('messages.json', 'r') as f:
    #         messages_dict = json.load(f)

    #     return messages_dict

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