from typing import Optional

class NotFoundException(Exception):
    """Exception raised when an object is not found."""
    def __init__(self, message: Optional[str] = "Object not found"):
        """Create a new NotFoundException instance.

        Args:
        --- 
            message (str, optional) : The error message. Has default message. 
        """
        self.message = message
        super().__init__(self.message)
