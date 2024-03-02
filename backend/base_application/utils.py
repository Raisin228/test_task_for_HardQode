class CustomError(Exception):
    """Для создания своих собственных исключений"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
