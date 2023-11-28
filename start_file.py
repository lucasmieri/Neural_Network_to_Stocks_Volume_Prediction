import os

# Define the project structure in a dictionary format
project_structure = {
    "projeto_predicao_volume": {
        "data": {},
        "notebooks": {},
        "src": {
            "__init__.py": "",
            "data.py": "# Scripts to load and preprocess data\n",
            "features.py": "# Scripts for feature engineering\n",
            "model.py": "# Neural network model definitions\n",
            "train.py": "# Script for model training\n",
            "evaluate.py": "# Script for evaluation and testing the model\n",
        },
        "tests": {
            "__init__.py": "",
            "test_data.py": "# Tests for the data module\n",
        },
        "requirements.txt": "# Project dependencies\n",
        "README.md": "# Project Documentation\n",
    }
}



# Function to create directories and files based on the project structure
def create_structure(base_path, structure):
    for name, value in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, value)  # Recursive call for subdirectories
        else:
            if not os.path.isfile(path):  # Check if file does not already exist
                with open(path, 'w') as file:
                    file.write(value)
            else:
                print(f"File {path} already exists. Skipping...")

# Base path for creating the structure
base_path = os.getcwd()

# Create the project structure
create_structure(base_path, project_structure)

# Verify the structure by listing the contents
created_paths = []  # List to hold the paths of created files and directories
for root, dirs, files in os.walk(base_path + "/Neural_Network_to_Stocks_Volume_Prediction", topdown=True):
    for name in dirs:
        dir_path = os.path.join(root, name)
        created_paths.append(dir_path)
        print(dir_path)
    for name in files:
        file_path = os.path.join(root, name)
        created_paths.append(file_path)
        print(file_path)

# Output created paths to a variable
created_paths