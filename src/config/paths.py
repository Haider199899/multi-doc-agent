import os
# Get the directory of the current script file
base_path = os.path.dirname(os.path.abspath(__file__))
# Get the directory of the current script file (config/paths.py)
current_script_path = os.path.dirname(os.path.abspath(__file__))

# Move up one level to reach the 'src' directory
base_path = os.path.dirname(current_script_path)

# Define the dynamic path for the documents folder
documents_folder_path = os.path.join(base_path, "../data/files/")
document_paths = [os.path.join(documents_folder_path,doc) for doc in os.listdir(documents_folder_path)]