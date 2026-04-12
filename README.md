# 🚀 AI Startup Simulator

An LLM-powered reinforcement-style environment where an AI agent runs a startup — making real decisions about hiring, product development, marketing, and fundraising.

Built for the **Meta PyTorch Hackathon x Scaler SST 2026**.

---

## 🧠 What Makes This Real-World Useful

Most RL environments are games. This simulates a **genuine business decision problem** — resource allocation under uncertainty — which is directly applicable to:
- Training business strategy agents
- Evaluating LLM decision-making quality
- Benchmarking agent planning ability

---

## 🎮 Environment Design

### State Space
| Variable | Type | Description |
|----------|------|-------------|
| money | float | Available cash ($) |
| product | float | Product development progress |
| team | int | Number of team members |
| round | int | Current round number |
| alive | bool | Whether startup is still running |

### Action Space
| Action | Effect |
|--------|--------|
| hire | +1 team, -$20 |
| develop | +2 product, -$10 |
| marketing | +1 product, +$10 revenue, -$15 |
| save | +$10 cash |
| loan | +$30 funding |

### Reward Shaping
reward = (money × 0.01) + (product × 0.05) + (team × 0.03)
Clipped to (0.01, 0.99) — never exactly 0 or 1.

---

## 📊 Tasks & Graders

| Task | Difficulty | Goal | Success Criteria |
|------|-----------|------|-----------------|
| startup-survival | Easy | Stay alive 5 rounds | money≥50, product≥5, team≥2 |
| product-launch | Medium | Launch product in 8 rounds | money≥80, product≥8, team≥3 |
| team-scaling | Hard | Scale team in 12 rounds | money≥100, product≥12, team≥4 |

Difficulty progression:
- Easy: starts with $100
- Medium: starts with $70
- Hard: starts with $40

---

## 🏗️ Project Structure
ai-startup-simulator/
├── inference.py     # Main entrypoint + FastAPI server
├── env.py           # Startup environment with Pydantic models
├── agent.py         # LLM-powered decision agent
├── metrics.py       # Scoring, grading, success evaluation
├── requirements.txt # Dependencies
├── Dockerfile       # Docker deployment
└── openenv.yaml     # OpenEnv spec
---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Status check |
| /reset | POST | Reset environment |
| /step | POST | Take action |
| /health | GET | Health check |

---

## 🔧 Tech Stack

- Python 3.9
- FastAPI + Uvicorn
- OpenAI-compatible LLM (Qwen2.5-72B via HF Router)
- Pydantic typed models
- Docker on Hugging Face Spaces

---

## 👩‍💻 Author

**Suhani Soni** 
Meta PyTorch Hackathon x Scaler School of Technology,2026
