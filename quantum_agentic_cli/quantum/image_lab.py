from __future__ import annotations

import math
from typing import Any


class EntropyBanditEnvironment:
    def __init__(self, arms: int, seed: int = 0) -> None:
        self.arms = arms
        self.expected_rewards = [0.25 + 0.15 * i for i in range(arms)]
        self.reward_history: list[float] = []
        self.rng = __import__("random").Random(seed)

    def pull_arm(self, arm: int) -> float:
        mean = self.expected_rewards[arm]
        noise = self.rng.uniform(-0.2, 0.2)
        reward = max(0.0, min(1.0, mean + noise))
        self.reward_history.append(reward)
        return reward


class ImageEntropyFeatureExtractor:
    def __init__(self, image: Any) -> None:
        self.image = image

    def grayscale_array(self) -> list[int]:
        if hasattr(self.image, "getdata"):
            return [int(v) for v in self.image.getdata()]
        if isinstance(self.image, list):
            return [int(v) for v in self.image]
        return [0, 128, 255]

    def entropy(self) -> float:
        values = self.grayscale_array()
        if not values:
            return 0.0
        histogram = {}
        for pixel in values:
            histogram[pixel] = histogram.get(pixel, 0) + 1
        total = len(values)
        entropy = 0.0
        for count in histogram.values():
            p = count / total
            entropy -= p * math.log2(p) if p > 0 else 0.0
        return entropy


class AdaptiveImageTransformPolicy:
    def __init__(self) -> None:
        self.transformations = ["xor", "qft", "scramble"]

    def select(self, entropy: float) -> str:
        if entropy < 1.5:
            return "xor"
        if entropy < 3.0:
            return "qft"
        return "scramble"

    def apply(self, image_values: list[int], transform_name: str) -> list[int]:
        if transform_name == "xor":
            return [v ^ 0x55 for v in image_values]
        if transform_name == "qft":
            return [int((v + 13) % 256) for v in image_values]
        if transform_name == "scramble":
            return list(reversed(image_values))
        raise ValueError(f"Unsupported transformation: {transform_name}")
