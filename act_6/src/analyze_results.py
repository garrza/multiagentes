from owlready2 import *


def analyze_ontology_results(onto):
    """Analyze the results stored in the ontology"""

    print("\nDetailed Ontology Analysis:")

    # Count cells by type
    clean_cells = len(list(onto.CleanCell.instances()))
    dirty_cells = len(list(onto.DirtyCell.instances()))
    total_cells = len(list(onto.Cell.instances()))

    print(f"\nEnvironment Status:")
    print(f"Total Cells: {total_cells}")
    print(f"Clean Cells: {clean_cells}")
    print(f"Dirty Cells: {dirty_cells}")
    print(f"Cleanliness Percentage: {(clean_cells/total_cells)*100:.2f}%")

    # Analyze agent performance by type
    print("\nPerformance by Agent Type:")

    agent_types = [
        onto.BasicAgent,
        onto.SmartAgent,
        onto.EfficientAgent,
        onto.CollaborativeAgent,
    ]

    for agent_type in agent_types:
        agents = list(agent_type.instances())
        if agents:
            total_moves = sum(len(agent.has_moves_count) for agent in agents)
            total_cleaned = sum(len(agent.has_cells_cleaned) for agent in agents)
            avg_moves = total_moves / len(agents)
            avg_cleaned = total_cleaned / len(agents)

            print(f"\n{agent_type.name}:")
            print(f"Number of agents: {len(agents)}")
            print(f"Average moves: {avg_moves:.2f}")
            print(f"Average cells cleaned: {avg_cleaned:.2f}")
            print(
                f"Efficiency ratio: {avg_cleaned/avg_moves if avg_moves > 0 else 0:.3f}"
            )

    # Analyze cell coverage
    print("\nCell Coverage Analysis:")
    unvisited_cells = [
        cell for cell in onto.Cell.instances() if len(cell.has_visited) == 0
    ]
    most_visited_cell = max(onto.Cell.instances(), key=lambda x: len(x.has_visited))

    print(f"Unvisited cells: {len(unvisited_cells)}")
    print(
        f"Most visited cell: ({most_visited_cell.has_x_coordinate[0]}, "
        f"{most_visited_cell.has_y_coordinate[0]}) "
        f"with {len(most_visited_cell.has_visited)} visits"
    )


def main():
    # Instead of loading from URL, we'll create a new ontology instance
    onto = get_ontology("http://vacuum.cleaner.ontology/")

    from .main import run_ontology_simulation

    simulation_results = run_ontology_simulation()

    # Use the ontology from the simulation
    analyze_ontology_results(simulation_results.onto)


if __name__ == "__main__":
    main()
