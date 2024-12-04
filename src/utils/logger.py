from loguru import logger
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logger.add("logs/app.logs", 
           colorize=True, 
           format="<green>{time}</green> <level>{message}</level>", 
           level="INFO",
           rotation="1 week", 
           retention="1 month",
           compression="zip"
           )
