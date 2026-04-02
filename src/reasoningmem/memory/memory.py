from array import array
from dataclasses import dataclass

@dataclass
class Memory:
    assumptions: list[str]
    thought: list[str]
    hypothesis: list[str]
    action: list[str]
    embedding: array[float]
