import networkx as nx
import pandas as pd


def create_campus_graph():

    locations = pd.read_csv("data/locations.csv")
    paths = pd.read_csv("data/paths.csv")

    graph = nx.Graph()

    # Add campus locations
    for _, row in locations.iterrows():

        graph.add_node(
            row["id"],
            name=row["name"]
        )

    # Connect campus locations
    for _, row in paths.iterrows():

        graph.add_edge(
            row["source"],
            row["destination"],
            weight=row["distance"]
        )

    return graph, locations


def find_shortest_route(start, end):

    graph, locations = create_campus_graph()

    route = nx.shortest_path(
        graph,
        source=start,
        target=end,
        weight="weight"
    )

    distance = nx.shortest_path_length(
        graph,
        source=start,
        target=end,
        weight="weight"
    )

    return route, distance, locations