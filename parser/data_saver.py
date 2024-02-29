import json
import logging


class DataSaver:
    """
    Class for saving data to JSON file.
    """

    @staticmethod
    def save_to_json(data, filename: str = "product_info.json") -> None:
        """
        Save data to a JSON file.

        Parameters:
        - data: The data to be saved.
        - filename (str): The name of the JSON file. Defaults to "product_info.json".
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved data to {filename}.")
