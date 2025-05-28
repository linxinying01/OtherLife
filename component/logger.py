import os
from loguru import logger

def setup_logger(log_path=None, log_level="DEBUG"):
    logger.add(os.path.join(log_path, "app.log"), rotation="100 MB",
           retention="7 days", level=log_level)
    

if __name__ == "__main__":
    setup_logger("logs")
    
    logger.trace("This is a trace message")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.success("This is a success message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")