import unittest
import pandas as pd
import json
import tempfile
from regression_analysis import validate_data
import os
from regression_analysis import (
    load_config,
    DEFAULT_CONFIG,
    check_unusual_values
)
from unittest.mock import patch


class TestValidation(unittest.TestCase):

    def test_valid_data(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [4.5, 6.2],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertEqual(problems, [])

    def test_negative_unemployment(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [-5.0, 6.2],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertIn(
            "Negative unemployment values found.",
            problems
        )

    def test_multiple_problems(self):
        data = {
            "country": ["Nigeria", "Nigeria"],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [-5.0, 6.2],
            "inflation": [24.0, None]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertIn("Missing values found.", problems)
        self.assertIn("Negative unemployment values found.", problems)
        self.assertIn("Duplicate country names found.", problems)

    def test_missing_country_name(self):
        data = {
            "country": ["Nigeria", None],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [4.5, 6.2],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertIn("Missing values found.", problems)
        self.assertIn("Missing country names found.", problems)

    def test_empty_country_name(self):
        data = {
            "country": ["Nigeria", "   "],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [4.5, 6.2],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertIn("Empty country names found.", problems)

    def test_missing_required_column(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [3.2, 4.0],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertTrue(
            any("Missing required columns:" in problem
                for problem in problems)
        )

    def test_all_required_columns_present(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [4.5, 6.2],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertEqual(problems, [])

    def test_non_numeric_unemployment(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [4.5, "unknown"],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertIn(
            "Non-numeric values found in unemployment.",
            problems)
        
    def test_unemployment_above_100(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [3.2, 4.0],
            "unemployment": [4.5, 105.0],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertIn(
            "Unemployment values above 100% found.",
            problems
        )

    def test_negative_gdp_growth_is_valid(self):
        data = {
            "country": ["Nigeria", "Ghana"],
            "GDP_growth": [-2.5, 4.0],
            "unemployment": [4.5, 6.2],
            "inflation": [24.0, 22.0]
        }

        df = pd.DataFrame(data)
        problems = validate_data(df)

        self.assertEqual(problems, [])

    def test_high_inflation_warning(self):
        df = pd.DataFrame({
            "country": ["Ghana"],
            "GDP_growth": [3.0],
            "unemployment": [6.0],
            "inflation": [60.0]
        })

        warnings = check_unusual_values(df)

        self.assertEqual(len(warnings), 1)
        self.assertIn("Ghana", warnings[0])
        self.assertIn("unusually high", warnings[0])
    

class TestLoadConfig(unittest.TestCase):

    def test_load_valid_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            config_path = os.path.join(temp_dir, "config.json")

            test_config = {
                "inflation_limit": 30,
                "GDP_growth_limit": -5
            }

            with open(config_path, "w") as file:
                json.dump(test_config, file)
            original_directory = os.getcwd()

            try:
                os.chdir(temp_dir)
                result = load_config()

            finally:
                os.chdir(original_directory)

            self.assertEqual(result, test_config)

    def test_missing_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            original_directory = os.getcwd()

            try:
                os.chdir(temp_dir)

                with patch("builtins.print") as mock_print:
                    result = load_config()

            finally:
                os.chdir(original_directory)

            self.assertEqual(result, DEFAULT_CONFIG)

            mock_print.assert_called_once_with(
                "Configuration file not found."
            )

    def test_invalid_json_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            config_path = os.path.join(temp_dir, "config.json")

            with open(config_path, "w") as file:
                file.write('{"inflation_limit": 30,}')

            original_directory = os.getcwd()

            try:
                os.chdir(temp_dir)

                with patch("builtins.print") as mock_print:
                    result = load_config()

            finally:
                os.chdir(original_directory)

            self.assertEqual(result, DEFAULT_CONFIG)

            mock_print.assert_called_once_with(
                "Invalid JSON configuration."
            )

    def test_missing_config_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            config_path = os.path.join(temp_dir, "config.json")

            test_config = {
                "inflation_limit": 30
            }

            with open(config_path, "w") as file:
                json.dump(test_config, file)

            original_directory = os.getcwd()

            try:
                os.chdir(temp_dir)
                result = load_config()

            finally:
                os.chdir(original_directory)

            expected_config = {
                "inflation_limit": 30,
                "GDP_growth_limit": -10
            }

            self.assertEqual(result, expected_config)

   
        

if __name__ == "__main__":
    unittest.main()