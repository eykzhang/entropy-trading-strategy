import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from alpaca.data.live import StockDataStream

# Load .env from parent directory of current file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

async def main():
    # Initialize stream client
    stream = StockDataStream(API_KEY, SECRET_KEY)

    # Define async handler for quote updates
    async def quote_handler(data):
        print(f"Quote update: {data}")

    # Subscribe to quotes for AAPL
    stream.subscribe_quotes(quote_handler, "AAPL")

    # Start streaming task
    task = asyncio.create_task(stream._run_forever())

    try:
        # Run for 10 seconds, then timeout
        await asyncio.wait_for(task, timeout=10.0)
    except asyncio.TimeoutError:
        print("Timeout reached, stopping stream...")
        await stream.stop()

if __name__ == "__main__":
    asyncio.run(main())