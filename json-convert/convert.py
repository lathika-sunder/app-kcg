import json

# Load JSON data from a file
with open('input.json', 'r') as file:
    data = json.load(file)

initial_nodes = []

for control in data["mockup"]["controls"]["control"]:
    if "children" in control and "controls" in control["children"] and "control" in control["children"]["controls"]:
        children_controls = control["children"]["controls"]["control"]
        for index, child in enumerate(children_controls):
            if "properties" in child and "text" in child["properties"]:
                text = child["properties"]["text"]
                node_id = f"{control['ID']}-{index}"
                node = {
                    "id": node_id,
                    "data": {"label": text},
                    "position": {"x": 900, "y": 100 + index * 100}  # Adjust y position as needed
                }
                initial_nodes.append(node)

# Create nodes JSON format
nodes_data = initial_nodes

# Save nodes data to a new JSON file
with open("nodes.json", "w") as nodes_file:
    json.dump(nodes_data, nodes_file, indent=2)

print("Nodes JSON file created successfully.")
