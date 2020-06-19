from rest_framework import status


class SuccessMessages:
    def __init__(self):
        self.message = "success"

    def inserted(self, *args):
        return "{} inserted successfully".format(" ".join(args))


class ErrorsMessages:
    def __init__(self):
        self.message = "error"
        self.invalid_post = "json post invalid according to the contract"
        self.json_keys = "The json post's keys are invalid according the contract"
        self.json_types = "The json post value's types are invalid according the contract"

    def not_found(self, name):
        return "{} not found".format(name)
