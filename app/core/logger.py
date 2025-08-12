from loguru import logger
import sys

# Remove the default handler
logger.remove()

# Add file handler with file path and line info
logger.add(
    "logs/sahiloan.log",                    # Log file name
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{function}:{line} | {message}",  # Log format with file info
    level="INFO",                 # Minimum log level
    rotation="10 MB",             # Rotate when file reaches 10MB
    retention="7 days",           # Keep logs for 7 days
    compression="zip",            # Compress rotated files
    backtrace=True,               # Enable backtrace for exceptions
    diagnose=True                 # Enable detailed error diagnosis
)

# Optional: Also keep console output with file info
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{file}:{function}:{line}</cyan> | {message}",
    level="INFO"
)