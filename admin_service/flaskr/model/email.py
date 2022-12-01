from datetime import datetime

class Email:
    def __init__(self, email_id: str, sender: str, sent_time: str, body: str, 
                 responded_time: str = None):
        self.id = email_id
        self.sender = sender
        self.sent_time = sent_time
        self.body = body
        self.responded_time = responded_time

    def to_json(self):
        return {"id": self.id,
                "sender": self.sender,
                "sent_time": self.sent_time,
                "body": self.body,
                "responded_time": self.responded_time}