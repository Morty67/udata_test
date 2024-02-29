import os
import json


def load_products():
    """
    Load product information from a JSON file.

    This function reads product information from a JSON file named "product_info.json"
    located in the root directory of the project. It returns the loaded
    information as a dictionary.

    Returns:
        dict: A dictionary containing product information loaded from the JSON file.

    Raises:
        FileNotFoundError: If the "product_info.json" file is not found.
        json.JSONDecodeError: If the content of the JSON file cannot be decoded.
    """
    # Directory path of the project root
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))  # два рівня вище кореневої папки

    # Full path to product_info.json file
    file_path = os.path.join(project_root, "product_info.json")

    # Read information from the product_info.json file
    with open(file_path, "r") as file:
        products = json.load(file)

    return products
