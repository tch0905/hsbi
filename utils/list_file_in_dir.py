import os

def list_files_in_directory(directory):
    """
    List all files in a directory.

    Parameters:
    - directory: Path to the directory.

    Returns:
    - files_list: List of files in the directory.
    """
    try:
        files_list = os.listdir(directory)
        return files_list
    except FileNotFoundError:
        print("Directory not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None