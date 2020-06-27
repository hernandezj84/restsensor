"""Module for success messages"""


class SuccessMessages:
    """Object with success messages"""

    def __init__(self):
        self.message = "success"

    def inserted(self, *args):
        """Inserted message """
        return "{} inserted successfully".format(" ".join(args))
