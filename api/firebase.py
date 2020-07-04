"""Updates firebase database"""
import pyrebase


class Firebase:
    """Exposes firebase crud executions"""

    def __init__(self):
        self.config = {
            "apiKey": "AIzaSyB4_wqwa2JirmifOC2YKIc3HQNMEy0DTtI",
            "databaseURL": "https://sensorgasglp-59be6.firebaseio.com/",
            "authDomain": "sensorgasglp-59be6.firebaseapp.com",
            "storageBucket": "sensorgasglp-59be6.appspot.com"
        }
        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()

    def set_event(self, json_post):
        """Updates the new event in firebase"""
        new_json_post = json_post.copy()
        new_json_post.pop("device_id")
        self.db.child(json_post["device_id"]).set(new_json_post)
