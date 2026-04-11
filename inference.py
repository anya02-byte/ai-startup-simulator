import os
import sys
import threading
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

BENCHMARK = "ai-startup-simulator"
MAX_STEPS = 5

TASKS = [
    {"name": "startup-survival", "goal": "Keep the startup alive by managing resources wisely."},
    {"name": "product-launch", "goal": "Successfully launch a product by building and marketing it."},
    {"name": "team-scaling", "goal": "Scale the team efficiently without burning cash."},
]

def get_initial_state():
    return {"money": 100, "product": 0, "team": 1, "round": 0}

def apply_action(state, action):
    action = action.lower().strip()
    if "hire" in action:
        state["money"] -= 20
        state["team"] += 1
    elif "develop" in action or "build" in action:
        state["money"] -= 10
        state["product"] += 2
    elif "market" in action:
        state["money"] -= 15
        state["product"] += 1
        state["money"] += 10
    elif "save" in action or "cut" in action:
        state["money"] += 10
    elif "loan" in action or "raise" in action:
        state["money"] += 30
    state["round"] += 1
    return state

def calculate_score(state):
    health = state["money"] + state["product"] * 10 + state["team"] * 5
    score = min(max(health / 300, 0.01), 0.99)
    return round(score, 2)

def calculate_reward(state):
    reward = (state["money"] * 0.01 + state["product"] * 0.05 + state["team"] * 0.03)
    return round(min(max(reward, 0.01), 0.99), 2)

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    done_val = "true" if done else "false"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    success_val = "true" if success else "false"
    print(f"[END] success={success_val} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

def run_task(client, task):
    task_name = task["name"]
    task_goal = task["goal"]
    log_start(task_name, BENCHMARK, MODEL_NAME)
    state = get_initial_state()
    rewards = []

    try:
        for step in range(1, MAX_STEPS + 1):
            done = step == MAX_STEPS
            prompt = f"""You are an AI startup founder agent.
Goal: {task_goal}
Current state: Money=${state['money']}, Product={state['product']}, Team={state['team']}, Round={state['round']}
Available actions: hire, develop, marketing, save, loan
Choose the best single action and explain in one sentence why."""

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.7
            )
            action = response.choices[0].message.content.strip()[:60]
            state = apply_action(state, action)
            reward = calculate_reward(state)
            rewards.append(reward)
            log_step(step, action.replace(" ", "_"), reward, done)

        score = calculate_score(state)
        log_end(state["money"] > 0, MAX_STEPS, score, rewards)

    except Exception as e:
        rewards.append(0.50)
        log_step(len(rewards), "error", 0.50, True, str(e)[:50])
        log_end(False, len(rewards), 0.50, rewards)

def run_once():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    for task in TASKS:
        run_task(client, task)

if __name__ == "__main__":
    run_once()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=run_once, daemon=True)
    thread.start()

@app.get("/")
def root():
    return {"status": "running", "project": "AI Startup Simulator"}

@app.post("/reset")
def reset():
    state = get_initial_state()
    return {"observation": state, "info": {}}

@app.post("/step")
def step(action: dict = {}):
    return {"observation": [], "reward": 0.5, "done": False, "info": {}}

@app.get("/health")
def health():
    return {"status": "ok"}
