from dataclasses import dataclass


@dataclass
class Problem:
    url: str
    name: str
    difficulty: str
    tags: list[str]
