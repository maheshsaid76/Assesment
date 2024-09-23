import ast

class FunctionSummarizer(ast.NodeVisitor):
    def __init__(self):
        self.summaries = {}  # Store function summaries
        self.functions_ast = {}  # Store the AST for each function

    def visit_FunctionDef(self, node):
        # Extract function name and arguments
        func_name = node.name
        args = [arg.arg for arg in node.args.args]

        # Store the AST for the function
        self.functions_ast[func_name] = node

        # Find dependencies (other function calls within this function)
        dependencies = self.find_dependencies(node)

        # Generate summary for the function
        summary = {
            "name": func_name,
            "args": args,
            "dependencies": dependencies,
            "docstring": ast.get_docstring(node)  # Extract docstring if available
        }
        # Store summary
        self.summaries[func_name] = summary

        # Continue visiting other nodes in the tree
        self.generic_visit(node)

    def find_dependencies(self, node):
        """Find other functions that are called within this function."""
        return [n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]

# Sample Python code to analyze
source_code = """
def helper_function(x):
    return x * 2

def main_function(a, b):
    return helper_function(a) + b
"""

# Parse the code into an AST
tree = ast.parse(source_code)

# Initialize the summarizer and visit the nodes
summarizer = FunctionSummarizer()
summarizer.visit(tree)

# Output the summaries and ASTs
print("Function Summaries:")
print(summarizer.summaries)

print("\nFunction ASTs:")
print(summarizer.functions_ast)
