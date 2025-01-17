from typing import Dict, List, Tuple
import random
from .base import Agent
from ..environment import Environment
from ..ontology import get_cell_at_position


class EfficientAgent(Agent):
    def __init__(self, position: Tuple[int, int], onto_agent):
        super().__init__(position, onto_agent)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.visited_cells = set()
        self.visited_cells.add(position)
        self.dirty_cells = set()

    def see(self, environment: Environment) -> Dict:
        current_cell = environment.get_cell_state(self.position)
        surroundings = self._get_surroundings(environment)
        return {"current": current_cell, "surroundings": surroundings}

    def next(self, perception: Dict) -> str:
        if perception["current"] == 1:
            return "CLEAN"

        # Update knowledge of dirty cells from surroundings
        for i, (dx, dy) in enumerate(self.directions):
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if perception["surroundings"][i] == 1:
                self.dirty_cells.add((new_x, new_y))

        return "MOVE"

    def action(self, action_type: str, environment: Environment) -> None:
        if action_type == "CLEAN":
            environment.clean_cell(self.position)
            self.cells_cleaned += 1
            self.dirty_cells.discard(self.position)
            # Update ontology
            cell = get_cell_at_position(self.onto_agent.namespace, *self.position)
            if isinstance(cell, self.onto_agent.namespace.DirtyCell):
                cell.is_a = [self.onto_agent.namespace.CleanCell]

        elif action_type == "MOVE":
            new_position = self._efficient_move(environment)
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

    def _efficient_move(self, environment: Environment) -> Tuple[int, int]:
        if self.dirty_cells:
            # Move towards nearest known dirty cell
            target = min(
                self.dirty_cells,
                key=lambda x: abs(x[0] - self.position[0])
                + abs(x[1] - self.position[1]),
            )
            dx = target[0] - self.position[0]
            dy = target[1] - self.position[1]

            # Move one step towards target
            new_x = self.position[0] + (1 if dx > 0 else -1 if dx < 0 else 0)
            new_y = self.position[1] + (1 if dy > 0 else -1 if dy < 0 else 0)

            if environment.is_valid_position((new_x, new_y)):
                return (new_x, new_y)

        # If no known dirty cells, explore systematically
        for dx, dy in self.directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if (
                environment.is_valid_position((new_x, new_y))
                and (new_x, new_y) not in self.visited_cells
            ):
                return (new_x, new_y)

        # If all adjacent cells visited, move randomly
        valid_moves = self._get_valid_moves(environment)
        return random.choice(valid_moves) if valid_moves else self.position

    def _get_surroundings(self, environment: Environment) -> List[int]:
        surroundings = []
        for dx, dy in self.directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if environment.is_valid_position((new_x, new_y)):
                surroundings.append(environment.get_cell_state((new_x, new_y)))
            else:
                surroundings.append(-1)
        return surroundings

    def _get_valid_moves(self, environment: Environment) -> List[Tuple[int, int]]:
        valid_moves = []
        for dx, dy in self.directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if environment.is_valid_position((new_x, new_y)):
                valid_moves.append((new_x, new_y))
        return valid_moves
