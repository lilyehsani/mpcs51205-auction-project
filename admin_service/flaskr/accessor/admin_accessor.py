import pymongo
from bson import ObjectId
from datetime import datetime

from flaskr.model.email import Email

db_address: str = "admin_db:27017"  # Needs to be the mongo docker container's name
db_name: str = "admindb"
table_name: str = "emails"

class AdminAccessor:
    def __init__(self):
        self.client = pymongo.MongoClient(db_address)
        self.db = self.client[db_name]
        self.table = self.db[table_name]

    def create_email(self, sender: str, sent_time: datetime, body: str):
        email = {"sender": sender,
                 "sent_time": format_time(sent_time),
                 "body": body, 
                 "responded_time": None}
        return self.table.insert_one(email).inserted_id

    def get_email_by_id(self, email_id: str):
        existing_email = self.table.find_one({"_id": ObjectId(email_id)})
        if not existing_email:
            raise Exception("This email does not exist.")
        
        return Email(str(existing_email.get("_id")), existing_email.get("sender"),
                         existing_email.get("sent_time"), existing_email.get("body"), 
                         existing_email.get("responded_time"))

    def get_all_email(self) -> list:
        emails = []
        for email_entry in self.table.find({}):
            email = Email(str(email_entry.get("_id")), email_entry.get("sender"),
                          email_entry.get("sent_time"), email_entry.get("body"), 
                          email_entry.get("responded_time"))
            emails.append(email)
        return emails

    def update_email(self, email_id: str, field_name: str, new_value):
        query = {"_id": ObjectId(email_id)}
        existing_email = self.table.find_one(query)
        if not existing_email:
            raise Exception("This email does not exist.")

        self.table.update_one(query,
                              {"$set": {field_name: new_value}})

    
def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')