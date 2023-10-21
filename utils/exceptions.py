class NotAuthenticatedException(Exception):
    def __init__(self, message: str = "Not authenticated in FutbolCompartir"):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
