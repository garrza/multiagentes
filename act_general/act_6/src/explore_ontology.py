from ontology import create_vacuum_ontology, initialize_environment
from owlready2 import *
import os


def explore_ontology():
    # Create generated directory if it doesn't exist
    generated_dir = os.path.join(os.path.dirname(__file__), "..", "generated")
    os.makedirs(generated_dir, exist_ok=True)

    # Create the ontology
    onto = create_vacuum_ontology()

    # Initialize a small environment (5x5 grid with 30% dirty cells)
    cells = initialize_environment(onto, 5, 5, 0.3)

    # 1. Print basic statistics
    print("\n=== Ontology Statistics ===")
    print(f"Number of classes: {len(list(onto.classes()))}")
    print(f"Number of object properties: {len(list(onto.object_properties()))}")
    print(f"Number of data properties: {len(list(onto.data_properties()))}")

    # 2. Print all classes
    print("\n=== Classes ===")
    for cls in onto.classes():
        print(f"Class: {cls.name}")
        if len(cls.is_a) > 1:  # First element is usually the parent class
            print(f"  Restrictions: {cls.is_a[1:]}")

    # 3. Print cell information
    print("\n=== Cell Information ===")
    dirty_cells = list(onto.DirtyCell.instances())
    clean_cells = list(onto.CleanCell.instances())
    print(f"Total cells: {len(cells)}")
    print(f"Dirty cells: {len(dirty_cells)}")
    print(f"Clean cells: {len(clean_cells)}")

    # 4. Print adjacency information for a sample cell
    if cells:
        sample_cell = cells[0]
        print(f"\n=== Adjacent Cells for {sample_cell.name} ===")
        for adj_cell in sample_cell.is_adjacent_to:
            print(f"Adjacent to: {adj_cell.name}")

    # 5. Save the ontology to a file in generated folder
    output_path = os.path.join(generated_dir, "vacuum_ontology.owl")
    onto.save(file=output_path, format="rdfxml")
    print(f"\n=== Ontology saved to '{output_path}' ===")


if __name__ == "__main__":
    explore_ontology()
