from owlready2 import *


def create_vacuum_ontology():
    # Create a new ontology
    onto = get_ontology("http://vacuum.cleaner.ontology/")

    with onto:
        # Define main classes
        class Agent(Thing):
            pass

        class Environment(Thing):
            pass

        class Cell(Thing):
            pass

        class Action(Thing):
            pass

        # Define agent types
        class BasicAgent(Agent):
            pass

        class SmartAgent(Agent):
            pass

        class EfficientAgent(Agent):
            pass

        class CollaborativeAgent(Agent):
            pass

        # Define cell states
        class DirtyCell(Cell):
            pass

        class CleanCell(Cell):
            pass

        # Define actions
        class CleanAction(Action):
            pass

        class MoveAction(Action):
            pass

        # Define object properties
        class has_position(ObjectProperty):
            domain = [Agent]
            range = [Cell]

        class has_visited(ObjectProperty):
            domain = [Agent]
            range = [Cell]

        class can_perform(ObjectProperty):
            domain = [Agent]
            range = [Action]

        class is_adjacent_to(ObjectProperty):
            domain = [Cell]
            range = [Cell]
            symmetric = True

        # Define data properties
        class has_moves_count(DataProperty):
            domain = [Agent]
            range = [int]

        class has_cells_cleaned(DataProperty):
            domain = [Agent]
            range = [int]

        class has_x_coordinate(DataProperty):
            domain = [Cell]
            range = [int]

        class has_y_coordinate(DataProperty):
            domain = [Cell]
            range = [int]

        # Define some rules using equivalent_to
        class VisitedCell(Cell):
            equivalent_to = [Cell & has_visited.some(Agent)]

        class UnvisitedCell(Cell):
            equivalent_to = [Cell & Not(has_visited.some(Agent))]

    return onto


def initialize_environment(onto, width: int, height: int, dirty_percentage: float):
    """Initialize the environment with cells in the ontology"""
    import random

    # Create all cells as clean initially
    cells = []
    for x in range(width):
        for y in range(height):
            cell_name = f"cell_{x}_{y}"
            cell = onto.CleanCell(cell_name)  # Create as CleanCell by default
            cell.has_x_coordinate = [x]
            cell.has_y_coordinate = [y]
            cells.append(cell)

    # Set adjacent relationships
    for cell in cells:
        x = cell.has_x_coordinate[0]
        y = cell.has_y_coordinate[0]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height:
                adjacent_cell = next(
                    c
                    for c in cells
                    if c.has_x_coordinate[0] == new_x and c.has_y_coordinate[0] == new_y
                )
                cell.is_adjacent_to.append(adjacent_cell)

    # Make some cells dirty based on dirty_percentage
    num_dirty = int(len(cells) * dirty_percentage)
    cells_to_dirty = random.sample(cells, num_dirty)

    for cell in cells_to_dirty:
        # Change the cell type from CleanCell to DirtyCell
        cell.is_a = [onto.DirtyCell]

    return cells


def get_cell_at_position(onto, x: int, y: int):
    """Helper function to get cell at specific coordinates"""
    return next(
        cell
        for cell in onto.Cell.instances()
        if cell.has_x_coordinate == [x] and cell.has_y_coordinate == [y]
    )
