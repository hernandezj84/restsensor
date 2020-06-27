"""Modules that handles messages"""


class SuccessMessages:
    """Success Messages control"""

    def __init__(self):
        self.message = "success"

    def inserted(self, *args):
        """Message when is a successfull insert"""
        return "{} inserted successfully".format(" ".join(args))


class ErrorsMessages:
    """Error messages control"""

    def __init__(self):
        self.message = "error"
        self.invalid_post = "json post invalid according to the contract"
        self.integrity_error = "Fields doesn't corresponds to database"
        self.json_keys = "The json post's keys are invalid according the contract"
        self.json_types = "The json post value's types are invalid according the contract"

    def not_found(self, name):
        """Error message when api doesn't found something"""
        return "{} not found".format(name)
