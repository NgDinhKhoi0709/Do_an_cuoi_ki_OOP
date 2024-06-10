import ast

def extract_docstrings(file_path):
    """
    Trích xuất tất cả các docstring từ file Python.
    Args:
        file_path (str): Đường dẫn tới file Python cần trích xuất.
    Returns:
        list: Danh sách các docstring được trích xuất.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)

    docstrings = []

    # Trích xuất docstring từ mô-đun (file)
    module_docstring = ast.get_docstring(tree)
    if module_docstring:
        docstrings.append(f"Module: {module_docstring}")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            if docstring:
                if isinstance(node, ast.FunctionDef):
                    docstrings.append(f"Function {node.name}: {docstring}")
                elif isinstance(node, ast.ClassDef):
                    docstrings.append(f"Class {node.name}: {docstring}")

    return docstrings

# Sử dụng hàm để trích xuất docstring
file_path = 'assets/main.py'  # Thay thế bằng đường dẫn tới file của bạn
docstrings = extract_docstrings(file_path)

# In ra tất cả các docstring
for doc in docstrings:
    print(doc)
    print('-' * 80)  # Đường phân cách để dễ đọc
