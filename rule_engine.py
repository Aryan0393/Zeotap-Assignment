# rule_engine.py

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Left child (another Node)
        self.right = right     # Right child (another Node)
        self.value = value     # Value for operand nodes (e.g., "age > 30")

    def to_dict(self):
        # Converts the Node into a dictionary
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }
    @staticmethod
    def from_dict(node_dict):
        # Ensure the node_dict is not None
        if node_dict is None:
            return None

        # Extract common fields
        node_type = node_dict["type"]
        value = node_dict.get("value", None)

        # Only operators have left and right children, operands don't
        if node_type == "operator":
            left = Node.from_dict(node_dict.get("left"))
            right = Node.from_dict(node_dict.get("right"))
            return Node(node_type, left=left, right=right, value=value)

        # For operands, we don't have left and right
        elif node_type == "operand":
            return Node(node_type, value=value)

        # Handle unknown node types (optional)
        raise ValueError(f"Unknown node type: {node_type}")
    
    # rule_engine.py

def parse_rule_string_to_ast(rule_string):
    if 'AND' in rule_string:
        left_part, right_part = rule_string.split(' AND ', 1)
        return Node("operator", left=parse_rule_string_to_ast(left_part), right=parse_rule_string_to_ast(right_part), value="AND")
    elif 'OR' in rule_string:
        left_part, right_part = rule_string.split(' OR ', 1)
        return Node("operator", left=parse_rule_string_to_ast(left_part), right=parse_rule_string_to_ast(right_part), value="OR")
    else:
        return Node("operand", value=rule_string.strip())
