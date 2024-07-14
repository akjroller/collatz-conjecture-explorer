from fastapi import FastAPI, HTTPException
from middleware.blocklist_middleware import BlockListMiddleware
from utils.logger import logger
from routes import collatz, stats
from database.database import setup_database
import subprocess
from config import ADMIN_PASSWORD

app = FastAPI(
    title="The Collatz Conjecture Explorer",
    description="This API provides insights and data related to the Collatz Conjecture, supporting exploration and visualization of Collatz sequences. Updates to come!",
    version="0.0.1",
)

blocked_ips = []


def update_blocked_ips():
    global blocked_ips
    with open("blocked_ips.txt", "r") as f:
        blocked_ips = f.read().splitlines()


update_blocked_ips()

app.add_middleware(BlockListMiddleware, blocked_ips=blocked_ips)

app.include_router(collatz.router, prefix="/collatz", tags=["Collatz"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])


@app.on_event("startup")
def on_startup():
    setup_database()
    subprocess.Popen(["python", "collatz.py"])


@app.post(
    "/refresh_block_list/{password}",
    summary="Refresh the IP Block List",
    description="Refreshes the IP block list. Requires the correct password.",
)
def refresh_block_list(password: str):
    if password == ADMIN_PASSWORD:
        update_blocked_ips()
        logger.info("IP block list has been updated")
        return {"message": "Block list successfully updated"}
    else:
        raise HTTPException(status_code=403, detail="Incorrect password.")
