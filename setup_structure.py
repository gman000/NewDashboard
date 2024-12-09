import os
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
def create_file(path, content=""):
    with open(path, 'w') as file:
        file.write(content)
    print(f"Created file: {path}")
# Create the directory structure
directories = [
    "data_integration",
    "data_integration/database",
    "data_integration/services",
    "data_integration/config",
]
# Create __init__.py files content
init_content = """# This file makes the directory a Python package
"""
# Create the structure
for directory in directories:
    create_directory(directory)
    # Create __init__.py in each directory
    create_file(os.path.join(directory, "__init__.py"), init_content)
print("\nProject structure created successfully!")
print("Now you can copy your existing .py files into these directories.")