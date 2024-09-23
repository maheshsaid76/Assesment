import ast

class CodeSearch(ast.NodeVisitor):
    def __init__(self):
        self.index = {
            "functions": {},  # To store function names and their line numbers
            "variables": {},  # To store variables and their data types
            "classes": {},    # To store class names
            "data_types": {}  # To store variable data types
        }

    def visit_FunctionDef(self, node):
        # Store function names and their line numbers
        func_name = node.name
        self.index['functions'][func_name] = node.lineno
        self.generic_visit(node)  # Continue visiting other nodes

    def visit_Assign(self, node):
        # Detect and store variable assignments and their data types
        if isinstance(node.value, ast.Constant):  # Simple variables
            var_type = type(node.value.value).__name__
            for target in node.targets:
                if isinstance(target, ast.Name):  # Ensure it's a simple variable
                    self.index['variables'][target.id] = var_type
        self.generic_visit(node)

    def search(self, query, query_type="functions"):
        """Search for functions, variables, or data types."""
        # Search through the specified index and return matching results
        results = {k: v for k, v in self.index[query_type].items() if query in k}
        return results

# Sample Python code to analyze
code = """
def square(x: int) -> int:
    return x * x

y = 10
"""

# Parse the code into an AST
tree = ast.parse(code)

# Initialize the search mechanism and visit the nodes
searcher = CodeSearch()
searcher.visit(tree)

# Example searches
print("Search for functions:")
print(searcher.search("square", "functions"))

print("\nSearch for variables:")
print(searcher.search("y", "variables"))
