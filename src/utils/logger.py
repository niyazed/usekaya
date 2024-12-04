from loguru import logger

logger.add("logs/app.logs", 
           colorize=True, 
           format="<green>{time}</green> <level>{message}</level>", 
           level="INFO",
           rotation="1 week",
           retention="1 month",
           compression="zip"
           )
