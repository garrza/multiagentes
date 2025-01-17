from typing import Dict, List, Tuple
import random
from .base import Agent
from ..environment import Environment
from ..ontology import get_cell_at_position


class SmartAgent(Agent):
    def __init__(self, position: Tuple[int, int], onto_agent):
        super().__init__(position, onto_agent)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # More structured movement
        self.current_direction = 0
        self.visited_cells = set()
        self.visited_cells.add(position)

    def see(self, environment: Environment) -> Dict:
        current_cell = environment.get_cell_state(self.position)
        surroundings = self._get_surroundings(environment)
        return {"current": current_cell, "surroundings": surroundings}

    def next(self, perception: Dict) -> str:
        if perception["current"] == 1:
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
            new_position = self._smart_move(environment)
            if new_position:
                self.position = new_position
                self.moves_count += 1
                self.visited_cells.add(new_position)
                # Update ontology
                new_cell = get_cell_at_position(
                    self.onto_agent.namespace, *new_position
                )
                self.onto_agent.has_position = [new_cell]
                self.onto_agent.has_visited.append(new_cell)

    def _smart_move(self, environment: Environment) -> Tuple[int, int]:
        # Try to move in current direction
        dx, dy = self.directions[self.current_direction]
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        if not environment.is_valid_position((new_x, new_y)):
            # Change direction if we hit a wall
            self.current_direction = (self.current_direction + 1) % len(self.directions)
            dx, dy = self.directions[self.current_direction]
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy

        return (
            (new_x, new_y)
            if environment.is_valid_position((new_x, new_y))
            else self.position
        )

    def _get_surroundings(self, environment: Environment) -> List[int]:
        surroundings = []
        for dx, dy in self.directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if environment.is_valid_position((new_x, new_y)):
                surroundings.append(environment.get_cell_state((new_x, new_y)))
            else:
                surroundings.append(-1)  # Wall or invalid position
        return surroundings
