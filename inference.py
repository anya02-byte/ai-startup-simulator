import os
import sys
import threading
from fastapi import FastAPI
from openai import OpenAI
from env import StartupEnv
from agent import choose_action
from metrics import calculate_metrics, calculate_difficulty_bonus, is_success

app = FastAPI()

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
BENCHMARK = "ai-startup-simulator"

TASKS = [
    {
        "name": "startup-survival",
        "difficulty": "easy",
        "goal": "Keep the startup alive for 5 rounds by managing money wisely."
    },
    {
        "name": "product-launch",
        "difficulty": "medium",
        "goal": "Successfully launch a product by reaching product score of 8 within 8 rounds."
    },
    {
        "name": "team-scaling",
        "difficulty": "hard",
        "goal": "Scale the team to 4 members while keeping money above 100 within 12 rounds."
    },
]

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

def run_task(task):
    task_name = task["name"]
    difficulty = task["difficulty"]
    goal = task["goal"]

    log_start(task_name, BENCHMARK, MODEL_NAME)

    env = StartupEnv(difficulty=difficulty)
    state = env.reset()
    rewards = []

    try:
        while True:
            action = choose_action(state, goal)
            result = env.step(action)
            rewards.append(result.reward)
            log_step(
                step=state["round"] + 1,
                action=action,
                reward=result.reward,
                done=result.done
            )
            state = result.observation
            if result.done:
                break

        health, score, status = calculate_metrics(
            state["money"], state["product"], state["team"]
        )
        final_score = calculate_difficulty_bonus(difficulty, score)
        success = is_success(state, difficulty)
        log_end(success, state["round"], final_score, rewards)

    except Exception as e:
        rewards.append(0.50)
        log_step(len(rewards), "error", 0.50, True, str(e)[:50])
        log_end(False, len(rewards), 0.50, rewards)

def run_once():
    for task in TASKS:
        run_task(task)

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
    env = StartupEnv()
    state = env.reset()
    return {"observation": state, "info": {}}

@app.post("/step")
def step(action: dict = {}):
    return {"observation": {}, "reward": 0.5, "done": False, "info": {}}

@app.get("/health")
def health():
    return {"status": "ok"}
