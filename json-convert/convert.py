import json

# Load JSON data from a file
with open('input.json', 'r') as file:
    data = json.load(file)

initial_nodes = []
initial_edges = []

for control in data["mockup"]["controls"]["control"]:
    node_id = control["ID"]

    # Check if 'properties' key exists and contains 'text' key for label
    if "properties" in control and "text" in control["properties"]:
        label = control["properties"]["text"]
        node = {
            "id": node_id,
            "data": {"label": label},
            "position": {"x": int(control["x"]), "y": int(control["y"])}
        }

        initial_nodes.append(node)

        if control.get("children") and control["children"]["controls"]["control"]:
            for child in control["children"]["controls"]["control"]:
                edge_id = f"e{node_id}-{child['ID']}"
                edge = {"id": edge_id, "source": node_id, "target": child["ID"]}
                initial_edges.append(edge)

# Create nodes JSON format
nodes_data = {
    "nodes": initial_nodes
}

# Create edges JSON format
edges_data = {
    "edges": initial_edges
}

# Save nodes data to a new JSON file
with open("nodes.json", "w") as nodes_file:
    json.dump(nodes_data, nodes_file, indent=2)

# Save edges data to a new JSON file
with open("edges.json", "w") as edges_file:
    json.dump(edges_data, edges_file, indent=2)

print("Nodes and Edges JSON files created successfully.")
