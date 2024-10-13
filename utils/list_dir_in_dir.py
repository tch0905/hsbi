import os

def list_directories_in_directory(directory):
    if not os.path.isdir(directory):
        return "Invalid directory path."

    # Initialize a list to store directory names
    directory_list = []

    # List all items in the directory
    items = os.listdir(directory)

    # Append directory names to the list
    for item in items:
        if os.path.isdir(os.path.join(directory, item)):
            directory_list.append(item)

    return directory_list
