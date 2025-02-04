from ontology import create_vacuum_ontology
import graphviz
import os


def visualize_ontology():
    onto = create_vacuum_ontology()

    # Create generated directory if it doesn't exist
    generated_dir = os.path.join(os.path.dirname(__file__), "..", "generated")
    os.makedirs(generated_dir, exist_ok=True)

    # Create a new directed graph
    dot = graphviz.Digraph(comment="Vacuum Cleaner Ontology")
    dot.attr(rankdir="BT")  # Bottom to Top direction

    # Add class nodes
    for cls in onto.classes():
        dot.node(cls.name, cls.name)
        # Add inheritance edges
        for parent in cls.is_a:
            if hasattr(parent, "name"):  # Check if parent is a class
                dot.edge(cls.name, parent.name)

    # Save the graph in the generated folder
    output_path = os.path.join(generated_dir, "ontology_visualization")
    dot.render(output_path, format="png", cleanup=True)
    print(f"Visualization saved to {output_path}.png")


if __name__ == "__main__":
    visualize_ontology()
