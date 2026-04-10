import asyncio
import os
import uvicorn
from fastapi import FastAPI
import threading

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/reset")
def reset():
    return {"observation": [], "info": {}
            
@app.post("/step")
def step(action: dict = {}):
    return {
        "observation": [],
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.get("/health")
def health():
    return {"status": "ok"}

async def run_simulation():
    print("Starting OpenENV simulation...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("No API key found — running in offline mode")
    i = 1
    while True:
        print(f"Simulation step {i}")
        i += 1
        await asyncio.sleep(2)

def start_simulation():
    asyncio.run(run_simulation())

if __name__ == "__main__":
    sim_thread = threading.Thread(target=start_simulation, daemon=True)
    sim_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=7860)
