from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ArmResult:
    arm: int
    reward: float


@dataclass
class BanditEpisode:
    arm: int
    reward: float
    policy_probability: float
    exploration_rate: float
    parameter_update: float


class VariationalBanditAgent:
    def __init__(self, arms: int, seed: int = 0) -> None:
        self.arms = arms
        self.seed = seed
        self.random = random.Random(seed)
        self.parameters = [0.1 * (idx + 1) for idx in range(arms)]
        self.history: list[BanditEpisode] = []

    def encode_features(self, arm: int, reward_history: list[float]) -> float:
        mean_reward = sum(reward_history) / max(1, len(reward_history)) if reward_history else 0.0
        return (arm + 1) * 0.5 + mean_reward

    def parameterized_policy(self, arm: int, reward_history: list[float]) -> float:
        feature = self.encode_features(arm, reward_history)
        return 1.0 / (1.0 + math.exp(-(self.parameters[arm] + feature)))

    def select_arm(self, reward_history: list[float]) -> int:
        probs = [self.parameterized_policy(i, reward_history) for i in range(self.arms)]
        total = sum(probs)
        if total <= 0:
            return self.random.randrange(self.arms)
        weights = [p / total for p in probs]
        return self.random.choices(range(self.arms), weights=weights, k=1)[0]

    def run_episode(self, environment: Any, exploration_rate: float = 0.2) -> BanditEpisode:
        reward_history = environment.reward_history
        arm = self.select_arm(reward_history)
        reward = environment.pull_arm(arm)
        update = 0.1 * (reward - self.parameters[arm])
        self.parameters[arm] += update
        episode = BanditEpisode(
            arm=arm,
            reward=reward,
            policy_probability=self.parameterized_policy(arm, reward_history),
            exploration_rate=exploration_rate,
            parameter_update=update,
        )
        self.history.append(episode)
        return episode

    def evaluate(self, environment: Any, episodes: int = 25) -> dict[str, Any]:
        rewards = []
        regrets = []
        for _ in range(episodes):
            episode = self.run_episode(environment)
            rewards.append(episode.reward)
            regrets.append(max(environment.expected_rewards) - episode.reward)
        return {
            "episodes": episodes,
            "average_reward": sum(rewards) / max(len(rewards), 1),
            "total_regret": sum(regrets),
            "history": self.history,
            "parameters": self.parameters,
        }
