import openpyxl

def xlsx_to_markdown(xlsx_file_path):
    """
    Converts an Excel file to a Markdown string.

    Parameters:
    - xlsx_file_path: Path to the Excel file to convert.

    Returns:
    - markdown_string: The converted Markdown string.
    """
    try:
        # Load the Excel file
        wb = openpyxl.load_workbook(xlsx_file_path, data_only=True)

        markdown_string = ""

        # Iterate over all sheets in the workbook
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]

            # Get the data from the current sheet
            data = [[cell.value if cell.value is not None else "" for cell in row] for row in sheet.rows]

            # Add a header for the sheet
            markdown_string += f"**{sheet_name}**\n"
            markdown_string += "|"
            for header in data[0]:
                markdown_string += f" {header} |"
            markdown_string += "\n"
            markdown_string += "|"
            for _ in range(len(data[0])):
                markdown_string += "---|"
            markdown_string += "\n"
            for row in data[1:]:
                markdown_string += "|"
                for cell in row:
                    markdown_string += f" {cell} |"
                markdown_string += "\n"
            markdown_string += "\n"

        return markdown_string
    except FileNotFoundError:
        print("The file does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


