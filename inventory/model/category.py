category_status = {
    "normal": 0,
    "deleted": 1,
}

class Category:
    def __init__(self, id, name, status) -> None:
        self.id = id
        self.name = name
        self.status = status

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "status":self.status
        }