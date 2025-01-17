from ontology import create_vacuum_ontology, initialize_environment
from owlready2 import *


def query_ontology():
    onto = create_vacuum_ontology()
    cells = initialize_environment(onto, 5, 5, 0.3)

    # Prepare SPARQL prefix
    prefix = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX vc: <http://vacuum.cleaner.ontology/>
    """

    # Example queries
    queries = [
        """
        SELECT ?cell
        WHERE {
            ?cell rdf:type vc:DirtyCell
        }
        """,
        """
        SELECT ?cell ?x ?y
        WHERE {
            ?cell vc:has_x_coordinate ?x .
            ?cell vc:has_y_coordinate ?y
        }
        """,
    ]

    # Run queries
    world = onto.world
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i} results:")
        results = list(world.sparql_query(prefix + query))
        for result in results:
            print(result)


if __name__ == "__main__":
    query_ontology()
