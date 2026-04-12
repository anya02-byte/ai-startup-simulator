from openai import OpenAI
import os

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

ACTIONS = ["hire", "develop", "marketing", "save", "loan"]

def choose_action(state: dict, goal: str) -> str:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    prompt = f"""You are an AI startup founder agent.
Goal: {goal}
Current state:
- Money: ${state['money']}
- Product progress: {state['product']}
- Team size: {state['team']}
- Round: {state['round']}

Available actions: {', '.join(ACTIONS)}

Rules:
- If money < 20, prioritize save or loan
- If product < 5, prioritize develop
- If team < 3, consider hire

Reply with exactly one action word only. No explanation."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.3
        )
        action = response.choices[0].message.content.strip().lower()
        for a in ACTIONS:
            if a in action:
                return a
        return "save"
    except Exception:
        return "save"
