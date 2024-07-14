import os
import logging

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.FileHandler("logs/app.log")
handler.setFormatter(formatter)

logger.addHandler(handler)
