import csv


def csv_to_markdown(csv_file_path, markdown_file_path):
    """
    Converts a CSV file to Markdown format and saves it to a new file.

    Parameters:
    - csv_file_path: Path to the CSV file to convert.
    - markdown_file_path: Path where the Markdown file will be saved.
    """
    try:
        with open(csv_file_path, 'r') as csv_file, open(markdown_file_path, 'w') as markdown_file:
            csv_reader = csv.reader(csv_file)
            markdown_file.write('|')
            # Write headers
            for header in next(csv_reader):
                markdown_file.write(' {} |'.format(header))
            markdown_file.write('\n')
            # Write separator line
            markdown_file.write('|')
            for _ in range(len(next(csv_reader))):
                markdown_file.write(' --- |')
            markdown_file.write('\n')
            # Write rows
            for row in csv_reader:
                markdown_file.write('|')
                for cell in row:
                    markdown_file.write(' {} |'.format(cell))
                markdown_file.write('\n')
        print(f"CSV file converted to Markdown successfully. Saved as {markdown_file_path}")
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

