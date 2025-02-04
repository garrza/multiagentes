from typing import Dict, List, Tuple, Set
import random
from .base import Agent
from ..environment import Environment
from ..ontology import get_cell_at_position


class CollaborativeAgent(Agent):
    def __init__(self, position: Tuple[int, int], onto_agent):
        super().__init__(position, onto_agent)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.visited_cells = set()
        self.visited_cells.add(position)
        self.dirty_cells = set()
        self.assigned_quadrant = None
        self.other_agents_positions = set()

    def _get_unvisited_cells_in_quadrant(
        self, environment: Environment
    ) -> List[Tuple[int, int]]:
        """Get list of unvisited cells in the agent's assigned quadrant"""
        if not self.assigned_quadrant:
            return []

        width, height = environment.get_dimensions()
        quadrant_bounds = [
            ((0, 0), (width // 2, height // 2)),
            ((width // 2, 0), (width, height // 2)),
            ((0, height // 2), (width // 2, height)),
            ((width // 2, height // 2), (width, height)),
        ][self.assigned_quadrant]

        (x1, y1), (x2, y2) = quadrant_bounds
        unvisited = []

        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x, y) not in self.visited_cells and environment.is_valid_position(
                    (x, y)
                ):
                    unvisited.append((x, y))

        return unvisited

    def _get_quadrant_dirty_cells(self) -> Set[Tuple[int, int]]:
        if not self.assigned_quadrant:
            return set()

        return {cell for cell in self.dirty_cells if self._is_in_quadrant(cell)}

    def _is_in_quadrant(self, position: Tuple[int, int]) -> bool:
        if not self.assigned_quadrant:
            return False

        x, y = position
        width = self.environment.width
        height = self.environment.height

        quadrant_bounds = [
            ((0, 0), (width // 2, height // 2)),
            ((width // 2, 0), (width, height // 2)),
            ((0, height // 2), (width // 2, height)),
            ((width // 2, height // 2), (width, height)),
        ][self.assigned_quadrant]

        (x1, y1), (x2, y2) = quadrant_bounds
        return x1 <= x < x2 and y1 <= y < y2

    def see(self, environment: Environment) -> Dict:
        current_cell = environment.get_cell_state(self.position)
        surroundings = self._get_surroundings(environment)
        return {
            "current": current_cell,
            "surroundings": surroundings,
            "other_agents": self._get_other_agents_positions(environment),
        }

    def next(self, perception: Dict) -> str:
        if perception["current"] == 1:
            return "CLEAN"

        # Update knowledge of environment and other agents
        self.other_agents_positions = perception["other_agents"]
        self._update_dirty_cells(perception["surroundings"])

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
            if not self.assigned_quadrant:
                self._assign_quadrant(environment)

            new_position = self._collaborative_move(environment)
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

    def _collaborative_move(self, environment: Environment) -> Tuple[int, int]:
        # First priority: clean dirty cells in assigned quadrant
        quadrant_dirty_cells = self._get_quadrant_dirty_cells()
        if quadrant_dirty_cells:
            target = min(
                quadrant_dirty_cells,
                key=lambda x: abs(x[0] - self.position[0])
                + abs(x[1] - self.position[1]),
            )
            return self._move_towards(target, environment)

        # Second priority: explore unvisited cells in quadrant
        unvisited = self._get_unvisited_cells_in_quadrant(environment)
        if unvisited:
            target = min(
                unvisited,
                key=lambda x: abs(x[0] - self.position[0])
                + abs(x[1] - self.position[1]),
            )
            return self._move_towards(target, environment)

        # If quadrant is clean, help others
        return self._get_help_move(environment)

    def _move_towards(
        self, target: Tuple[int, int], environment: Environment
    ) -> Tuple[int, int]:
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]

        # Try to move in x direction
        if dx != 0:
            new_pos = (self.position[0] + (1 if dx > 0 else -1), self.position[1])
            if environment.is_valid_position(new_pos):
                return new_pos

        # Try to move in y direction
        if dy != 0:
            new_pos = (self.position[0], self.position[1] + (1 if dy > 0 else -1))
            if environment.is_valid_position(new_pos):
                return new_pos

        return self.position

    def _get_help_move(self, environment: Environment) -> Tuple[int, int]:
        # Find nearest dirty cell in any quadrant
        if self.dirty_cells:
            target = min(
                self.dirty_cells,
                key=lambda x: abs(x[0] - self.position[0])
                + abs(x[1] - self.position[1]),
            )
            return self._move_towards(target, environment)

        # If no known dirty cells, move randomly while avoiding other agents
        valid_moves = self._get_valid_moves(environment)
        valid_moves = [
            move for move in valid_moves if move not in self.other_agents_positions
        ]
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

    def _update_dirty_cells(self, surroundings: List[int]):
        for i, (dx, dy) in enumerate(self.directions):
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if surroundings[i] == 1:
                self.dirty_cells.add((new_x, new_y))
            elif surroundings[i] == 0:
                self.dirty_cells.discard((new_x, new_y))

    def _get_other_agents_positions(
        self, environment: Environment
    ) -> Set[Tuple[int, int]]:
        # This method should be implemented based on how your environment
        # provides information about other agents
        return set()

    def _get_valid_moves(self, environment: Environment) -> List[Tuple[int, int]]:
        valid_moves = []
        for dx, dy in self.directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if environment.is_valid_position((new_x, new_y)):
                valid_moves.append((new_x, new_y))
        return valid_moves

    def _assign_quadrant(self, environment: Environment) -> None:
        """Assign a quadrant to the agent based on its current position"""
        width, height = environment.get_dimensions()
        x, y = self.position

        # Determine quadrant based on current position
        if x < width // 2:
            if y < height // 2:
                self.assigned_quadrant = 0  # Top-left
            else:
                self.assigned_quadrant = 2  # Bottom-left
        else:
            if y < height // 2:
                self.assigned_quadrant = 1  # Top-right
            else:
                self.assigned_quadrant = 3  # Bottom-right

        # Store environment reference for quadrant calculations
        self.environment = environment
