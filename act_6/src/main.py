from .simulation import Simulation
from owlready2 import *


def run_ontology_simulation():
    # Simulation parameters
    width = 10
    height = 10
    num_agents = 4
    dirty_percentage = 0.3
    max_time = 100
    agent_type = "mixed"  # Can be "mixed", "collaborative", or "basic"

    # Create and run simulation
    simulation = Simulation(
        width=width,
        height=height,
        num_agents=num_agents,
        dirty_percentage=dirty_percentage,
        max_time=max_time,
        agent_type=agent_type,
    )

    # Run the simulation
    results = simulation.run()

    # Print results
    print("\nSimulation Results:")
    print(f"Initial dirty cells: {results['initial_dirty']}")
    print(f"Remaining dirty cells: {results['remaining_dirty']}")
    print(f"Cleaned cells: {results['cleaned_cells']}")
    print(f"Total moves: {results['total_moves']}")
    print(f"Time steps: {results['time_steps']}")
    print(f"Cleaning efficiency: {results['cleaning_efficiency']:.2f}%")

    # Query the ontology for additional insights
    onto = simulation.onto

    # Print agent statistics from ontology
    print("\nAgent Statistics from Ontology:")
    for agent in onto.Agent.instances():
        print(f"\nAgent: {agent.name}")
        print(
            f"Moves: {agent.has_moves_count[0] if len(agent.has_moves_count) > 0 else 0}"
        )
        print(
            f"Cells cleaned: {agent.has_cells_cleaned[0] if len(agent.has_cells_cleaned) > 0 else 0}"
        )
        print(
            f"Current position: ({agent.has_position[0].has_x_coordinate[0]}, "
            f"{agent.has_position[0].has_y_coordinate[0]})"
        )
        print(f"Cells visited: {len(agent.has_visited)}")

    return simulation  # Return the simulation object


def main():
    try:
        run_ontology_simulation()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e  # This will help see the full error trace


if __name__ == "__main__":
    main()
