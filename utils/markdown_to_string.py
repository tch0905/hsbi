def markdown_file_to_string(markdown_file_path):
    """
    Reads a Markdown file and returns its contents as a string.

    Parameters:
    - markdown_file_path: Path to the Markdown file to read.

    Returns:
    - markdown_string: The contents of the Markdown file as a string.
    """
    try:
        with open(markdown_file_path, 'r') as markdown_file:
            markdown_string = markdown_file.read()
            return markdown_string
    except FileNotFoundError:
        print("The file does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
