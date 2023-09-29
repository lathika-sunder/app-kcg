import json

# Load JSON data from a file
with open('input.json', 'r') as file:
    data = json.load(file)

initial_nodes = []

for control in data["mockup"]["controls"]["control"]:
    if "children" in control and "controls" in control["children"] and "control" in control["children"]["controls"]:
        children_controls = control["children"]["controls"]["control"]
        # Calculate the total width required for all nodes in children_controls
        total_width = sum([len(child.get("properties", {}).get("text", "")) for child in children_controls])
        # Calculate the initial X-coordinate for the first node
        start_x = 900 - total_width * 10  # Adjust the spacing between characters as needed (10 units used here)

        for index, child in enumerate(children_controls):
            if "properties" in child and "text" in child["properties"]:
                text = child["properties"]["text"]
                x=child["x"]
                y=child["y"]
                node_id = f"{control['ID']}-{index}"
                node_width = len(text) * 10  # Assuming each character occupies 10 units of width
                # node_x = start_x + (node_width / 2)  # Center the node text
                node = {
                    "id": node_id,
                    "data": {"label": text},
                    "position": {"x": x, "y": y}  # Adjust y position as needed
                }
                initial_nodes.append(node)
                # Update start_x for the next node
                start_x += node_width

# Create nodes JSON format
nodes_data = initial_nodes

# Save nodes data to a new JSON file
with open("nodes.json", "w") as nodes_file:
    json.dump(nodes_data, nodes_file, indent=2)

print("Nodes JSON file created successfully.")
