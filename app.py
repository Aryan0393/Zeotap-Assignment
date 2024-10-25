from flask import Flask, request, jsonify
from rule_engine import Node  # Ensure this imports correctly
from rule_engine import Node, parse_rule_string_to_ast

app = Flask(__name__)

# Example route for the home page
@app.route('/')
def home():
    return "Welcome to the Rule Engine!"

# Example route for creating a rule
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule_string')
    if not rule_string:
        return jsonify({"error": "No rule string provided"}), 400
    
    try:
        ast = parse_rule_string_to_ast(rule_string)
        return jsonify({"message": "Rule created!", "ast": ast.to_dict()})
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    data = request.get_json()
    rules = data.get('rules', [])
    operation = data.get('operation', 'AND')  # Default operation is AND

    if not rules or len(rules) < 2:
        return jsonify({"error": "At least two rules are required to combine"}), 400

    try:
        combined_rule = combine_multiple_rules(rules, operation)
        return jsonify({"message": "Rules combined!", "combined_rule": combined_rule.to_dict()}), 200
    except Exception as e:
        app.logger.error(f"Error combining rules: {e}")  # Log the error for debugging
        return jsonify({"error": f"Unexpected error: {e}"}), 500


# Helper function to combine rules into a single AST
def combine_multiple_rules(rules, operation):
    # Create the initial rule AST from the first rule string
    root = create_rule(rules[0])

    for rule in rules[1:]:
        new_rule_ast = create_rule(rule)  # Create AST from the next rule string
        # Combine the current AST with the new one using the specified operation
        root = Node("operator", left=root, right=new_rule_ast, value=operation)

    return root



@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    try:
        # Ensure the JSON data has 'ast' and 'data' fields
        json_data = request.get_json()
        if 'ast' not in json_data or 'data' not in json_data:
            return jsonify({"error": "Invalid input, 'ast' and 'data' are required"}), 400

        # Extract and validate AST and data
        ast = json_data['ast']
        data = json_data['data']
        
        # Convert AST dictionary into Node objects and evaluate
        rule_ast = Node.from_dict(ast)
        result = evaluate_ast(rule_ast, data)
        
        return jsonify({"result": result})
    except KeyError as e:
        return jsonify({"error": f"Missing key in input: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid rule or data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

import re 
def evaluate_ast(node, data):
    if node.type == "operand":
        # Print the condition being evaluated
        print(f"\nEvaluating operand: {node.value}")
        
        # Split the condition like "age == 35" or "department == 'Sales'"
        field, operator, value = re.split(r'([<>!=]=?)', node.value)
        field = field.strip()
        operator = operator.strip()
        value = value.strip()

        print(f"Extracted - Field: {field}, Operator: {operator}, Value: {value}")

        # Check if field exists in the data
        if field not in data:
            print(f"Field '{field}' not found in data: {data}")
            return False
        
        # Handle string comparisons (strip quotes)
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]  # Strip quotes

        # Print data being compared for debugging
        print(f"Comparing data[{field}] = {data[field]} with value = {value} (after stripping quotes)")

        # Convert value and compare based on the operator
        if operator == '==':
            result = data[field] == int(value) if field == "age" else data[field] == value
            print(f"Result of comparison: {data[field]} {operator} {value} -> {result}")
            return result

    elif node.type == "operator":
        print(f"\nEvaluating operator: {node.value}")
        left_result = evaluate_ast(node.left, data)
        right_result = evaluate_ast(node.right, data)
        
        print(f"Left result: {left_result}, Right result: {right_result}")
        return left_result and right_result if node.value == "AND" else left_result or right_result

    return False


if __name__ == '__main__':
    app.run(debug=True)
