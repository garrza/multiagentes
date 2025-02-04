import random
from typing import List, Tuple, Set


class Environment:
    def __init__(self, width: int, height: int, dirty_percentage: float):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.dirty_cells: Set[Tuple[int, int]] = set()
        self._initialize_dirty_cells(dirty_percentage)

    def _initialize_dirty_cells(self, dirty_percentage: float) -> None:
        """Initialize dirty cells based on the given percentage"""
        total_cells = self.width * self.height
        num_dirty_cells = int(total_cells * dirty_percentage)

        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        dirty_positions = random.sample(all_positions, num_dirty_cells)

        for x, y in dirty_positions:
            self.grid[x][y] = 1
            self.dirty_cells.add((x, y))

    def get_cell_state(self, position: Tuple[int, int]) -> int:
        """Get the state of a cell (0: clean, 1: dirty)"""
        x, y = position
        if self.is_valid_position(position):
            return self.grid[x][y]
        return -1  # Invalid position

    def clean_cell(self, position: Tuple[int, int]) -> None:
        """Clean a cell at the given position"""
        x, y = position
        if self.is_valid_position(position) and self.grid[x][y] == 1:
            self.grid[x][y] = 0
            self.dirty_cells.discard((x, y))

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """Check if a position is valid within the grid"""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def get_dirty_count(self) -> int:
        """Get the number of remaining dirty cells"""
        return len(self.dirty_cells)

    def get_clean_count(self) -> int:
        """Get the number of clean cells"""
        return (self.width * self.height) - len(self.dirty_cells)

    def get_dimensions(self) -> Tuple[int, int]:
        """Get the dimensions of the environment"""
        return self.width, self.height

    def get_dirty_cells(self) -> Set[Tuple[int, int]]:
        """Get the set of dirty cell positions"""
        return self.dirty_cells.copy()

    def get_grid(self) -> List[List[int]]:
        """Get a copy of the current grid state"""
        return [row[:] for row in self.grid]
