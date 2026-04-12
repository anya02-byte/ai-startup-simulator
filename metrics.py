from typing import Tuple

def calculate_metrics(money: float, product: float, team: int) -> Tuple[float, float, str]:
    health = money + product * 10 + team * 5
    score = round(min(max(health / 300, 0.01), 0.99), 2)

    if health > 200:
        status = "Excellent 🚀"
    elif health > 150:
        status = "Good 📈"
    elif health > 80:
        status = "Average ⚠️"
    else:
        status = "Critical 🔴"

    return health, score, status

def calculate_difficulty_bonus(difficulty: str, score: float) -> float:
    bonus = {"easy": 0.0, "medium": 0.05, "hard": 0.10}[difficulty]
    return round(min(score + bonus, 0.99), 2)

def is_success(state: dict, difficulty: str) -> bool:
    thresholds = {
        "easy": {"money": 50, "product": 5, "team": 2},
        "medium": {"money": 80, "product": 8, "team": 3},
        "hard": {"money": 100, "product": 12, "team": 4}
    }
    t = thresholds[difficulty]
    return (state["money"] >= t["money"] and
            state["product"] >= t["product"] and
            state["team"] >= t["team"])
