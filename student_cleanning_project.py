import pandas as pd


def load_csv(file_path):
    """Load a CSV file and return its data."""

    try:
        data = pd.read_csv(file_path)

        if data.empty:
            return {
                "success": False,
                "message": "The CSV file contains no data."
            }

        if len(data.columns) == 0:
            return {
                "success": False,
                "message": "The CSV file has no columns."
            }

        return {
            "success": True,
            "message": "CSV file loaded successfully.",
            "data": data
        }

    except FileNotFoundError:
        return {
            "success": False,
            "message": "The CSV file could not be found."
        }

    except pd.errors.EmptyDataError:
        return {
            "success": False,
            "message": "The CSV file is empty."
        }

    except pd.errors.ParserError:
        return {
            "success": False,
            "message": "The CSV file could not be parsed."
        }