from typing import Dict, List, Tuple
import random
from .base import Agent
from ..environment import Environment
from ..ontology import get_cell_at_position


class BasicAgent(Agent):
    def __init__(self, position: Tuple[int, int], onto_agent):
        super().__init__(position, onto_agent)
        self.directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

    def see(self, environment: Environment) -> Dict:
        current_cell = environment.get_cell_state(self.position)
        return {"current": current_cell}

    def next(self, perception: Dict) -> str:
        if perception["current"] == 1:  # Dirty cell
            return "CLEAN"
        return "MOVE"

    def action(self, action_type: str, environment: Environment) -> None:
        if action_type == "CLEAN":
            environment.clean_cell(self.position)
            self.cells_cleaned += 1
            # Update ontology
            cell = get_cell_at_position(self.onto_agent.namespace, *self.position)
            if isinstance(cell, self.onto_agent.namespace.DirtyCell):
                cell.is_a = [self.onto_agent.namespace.CleanCell]

        elif action_type == "MOVE":
            valid_moves = self._get_valid_moves(environment)
            if valid_moves:
                new_position = random.choice(valid_moves)
                self.position = new_position
                self.moves_count += 1
                # Update ontology
                new_cell = get_cell_at_position(
                    self.onto_agent.namespace, *new_position
                )
                self.onto_agent.has_position = [new_cell]
                self.onto_agent.has_visited.append(new_cell)

    def _get_valid_moves(self, environment: Environment) -> List[Tuple[int, int]]:
        valid_moves = []
        for dx, dy in self.directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if environment.is_valid_position((new_x, new_y)):
                valid_moves.append((new_x, new_y))
        return valid_moves
