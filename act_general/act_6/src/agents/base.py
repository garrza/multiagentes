from abc import ABC, abstractmethod
from typing import Dict, Tuple
from ..environment import Environment
from owlready2 import *


class Agent(ABC):
    def __init__(self, position: Tuple[int, int], onto_agent):
        self.position = position
        self.moves_count = 0
        self.cells_cleaned = 0
        self.onto_agent = onto_agent  # Reference to ontology agent instance

    @abstractmethod
    def see(self, environment: Environment) -> Dict:
        pass

    @abstractmethod
    def next(self, perception: Dict) -> str:
        pass

    @abstractmethod
    def action(self, action_type: str, environment: Environment) -> None:
        pass

    def update_ontology(self):
        """Update the ontology with agent's current state"""
        self.onto_agent.has_moves_count = [self.moves_count]
        self.onto_agent.has_cells_cleaned = [self.cells_cleaned]
