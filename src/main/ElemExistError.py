
class ElemExistError(Exception):
    """shift elem does not exist"""

    def __init__(self, shift):
        self.shift = shift
        super().__init__("shift does not exist")


