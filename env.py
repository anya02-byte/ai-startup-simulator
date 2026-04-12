from pydantic import BaseModel
from typing import List, Optional

class StartupState(BaseModel):
    money: float = 100.0
    product: float = 0.0
    team: int = 1
    round: int = 0
    alive: bool = True

class StepResult(BaseModel):
    observation: dict
    reward: float
    done: bool
    info: dict

class StartupEnv:
    def __init__(self, difficulty: str = "easy"):
        self.difficulty = difficulty
        self.max_steps = {"easy": 5, "medium": 8, "hard": 12}[difficulty]
        self.reset()

    def reset(self):
        if self.difficulty == "easy":
            self.state = StartupState(money=100, product=0, team=1)
        elif self.difficulty == "medium":
            self.state = StartupState(money=70, product=0, team=1)
        else:
            self.state = StartupState(money=40, product=0, team=1)
        return self.state.dict()

    def step(self, action: str) -> StepResult:
        action = action.lower().strip()

        if "hire" in action:
            self.state.money -= 20
            self.state.team += 1
        elif "develop" in action or "build" in action:
            self.state.money -= 10
            self.state.product += 2
        elif "market" in action:
            self.state.money -= 15
            self.state.product += 1
            self.state.money += 10
        elif "save" in action or "cut" in action:
            self.state.money += 10
        elif "loan" in action or "raise" in action:
            self.state.money += 30

        self.state.round += 1
        self.state.alive = self.state.money > 0
        done = not self.state.alive or self.state.round >= self.max_steps

        reward = self._calculate_reward()
        return StepResult(
            observation=self.state.dict(),
            reward=reward,
            done=done,
            info={"difficulty": self.difficulty, "alive": self.state.alive}
        )

    def _calculate_reward(self) -> float:
        score = (self.state.money * 0.01 +
                 self.state.product * 0.05 +
                 self.state.team * 0.03)
        return round(min(max(score, 0.01), 0.99), 2)
