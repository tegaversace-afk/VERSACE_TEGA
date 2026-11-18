import pandas as pd
from regression_analysis import validate_data

test_data = {
    "country": ["Nigeria", "Ghana"],
    "GDP_growth": [3.2, 4.0],
    "unemployment": [-5.0, 6.2],
    "inflation": [24.0, 22.0]
}

test_df = pd.DataFrame(test_data)

problems = validate_data(test_df)

assert "Negative unemployment values found." in problems

print("Test passed! Negative unemployment was detected.")
assert len(problems) == 1

# Create a valid dataset
valid_data = {
    "country": ["Nigeria", "Ghana"],
    "GDP_growth": [3.2, 4.0],
    "unemployment": [4.5, 6.2],
    "inflation": [24.0, 22.0]
}

valid_df = pd.DataFrame(valid_data)

# Validate the correct dataset
valid_problems = validate_data(valid_df)

# Confirm that no problems were found
assert valid_problems == []

print("Test passed! The valid dataset has no detected problems.")
# Create a dataset with multiple problems
bad_data = {
    "country": ["Nigeria", "Nigeria"],
    "GDP_growth": [3.2, 4.0],
    "unemployment": [-5.0, 6.2],
    "inflation": [24.0, None]
}

bad_df = pd.DataFrame(bad_data)

# Validate the dataset
bad_problems = validate_data(bad_df)

# Check that all three problems are detected
assert "Missing values found." in bad_problems
assert "Negative unemployment values found." in bad_problems
assert "Duplicate country names found." in bad_problems

print("Test passed! Multiple data-quality problems were detected.")