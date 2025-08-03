import sys
import traceback
from logger.custom_logger import CustomLogger

class CustomException(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message
        self.traceback = traceback.format_exc()

    def __str__(self):
        return f"{self.message}\nTraceback:\n{self.traceback}"

    def log_exception(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger = CustomLogger().get_logger(__file__)
        logger.error(f"Exception occurred: {self.message}\nTraceback:\n{formatted_traceback}")
        return formatted_traceback
    
if __name__ == "__main__":
    try:
        raise CustomException("This is a custom exception message.")
    except CustomException as e:
        e.log_exception()
        print(e)