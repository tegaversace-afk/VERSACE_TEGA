
# import pandas as pd
#import statsmodels.api as sm

# # Step 1: Create our dataset
# data = {
#     "country": ["Nigeria", "Ghana", "Kenya", "South Africa"],
#     "GDP_growth": [3.2, 4.0, 5.1, 1.9],
#     "unemployment": [4.5, 6.2, 5.0, 32.8]
# }

# # Step 2: Create the DataFrame
# df = pd.DataFrame(data)

# # Step 3: Select our variables
# X = df["GDP_growth"]
# Y = df["unemployment"]

# # Step 4: Add the intercept
# X = sm.add_constant(X)

# # Step 5: Build and fit the regression model
# model = sm.OLS(Y, X).fit()

# # Step 6: Display the results
# print(model.summary())

# print("GDP growth coefficient:")
# print(model.params["GDP_growth"])

# print("R-squared:")
# print(model.rsquared)

# print("GDP growth p-value:")
# print(model.pvalues["GDP_growth"])

# 

# import pandas as pd
# import statsmodels.api as sm

# df = pd.read_csv("economic_data.csv")

# print(df)

# X = df[["GDP_growth", "inflation"]]
# Y = df["unemployment"]

# print(X)
# print(Y)
# # Add the intercept
# X = sm.add_constant(X)

# # Fit the multiple regression model
# model = sm.OLS(Y, X).fit()

# # Display the regression results
# print(model.summary())

# print("GDP growth coefficient:")
# print(model.params["GDP_growth"])

# print("Inflation coefficient:")
# print(model.params["inflation"])

# print("R-squared:")
# print(model.rsquared)

# print("GDP growth p-value:")
# print(model.pvalues["GDP_growth"])

# print("Inflation p-value:")
# print(model.pvalues["inflation"])


# import pandas as pd

# # Load the CSV file
# df = pd.read_csv("economic_data.csv")

# # Check the number of rows and columns
# print("Dataset shape:")
# print(df.shape)

# # Display the column names
# print("\nColumn names:")
# print(df.columns)

# # Display information about the dataset
# print("\nDataset information:")
# df.info()

# # Check for missing values
# print("\nMissing values:")
# print(df.isnull().sum())


# import pandas as pd

# # Load the CSV file
# df = pd.read_csv("economic_data.csv")

# # Check numeric data types
# print("Data types:")
# print(df[["GDP_growth", "unemployment", "inflation"]].dtypes)

# # Check for negative unemployment values
# print("\nNegative unemployment values:")
# print((df["unemployment"] < 0).sum())

# # Check for negative inflation values
# print("\nNegative inflation values:")
# print((df["inflation"] < 0).sum())


# import pandas as pd

# # Load the CSV file
# df = pd.read_csv("economic_data.csv")

# # 1. Check for missing values
# print("Missing values:")
# print(df.isnull().sum())

# # 2. Check for empty country names
# print("\nEmpty country names:")
# print((df["country"].str.strip() == "").sum())

# # 3. Check for negative unemployment
# print("\nNegative unemployment values:")
# print((df["unemployment"] < 0).sum())

# # 4. Check for missing country names
# print("\nMissing country names:")
# print(df["country"].isnull().sum())


# import pandas as pd

# # Load the CSV file
# df = pd.read_csv("economic_data.csv")

# # Check for duplicate country names
# print("Duplicate country rows:")
# print(df["country"].duplicated().sum())

# # Display duplicate country records
# print("\nDuplicate country records:")
# print(df[df["country"].duplicated(keep=False)])


# import pandas as pd

# # Load the CSV file
# df = pd.read_csv("economic_data.csv")

# # Count completely duplicated rows
# print("Number of duplicate rows:")
# print(df.duplicated().sum())

# # Display completely duplicated rows
# print("\nDuplicate records:")
# print(df[df.duplicated(keep=False)])


# import pandas as pd


# def validate_data(df):
#     """Check the quality of an economic dataset."""

#     print("Dataset shape:")
#     print(df.shape)

#     print("\nMissing values:")
#     print(df.isnull().sum())

#     print("\nEmpty country names:")
#     print((df["country"].str.strip() == "").sum())

#     print("\nNegative unemployment values:")
#     print((df["unemployment"] < 0).sum())

#     print("\nDuplicate country names:")
#     print(df["country"].duplicated().sum())

#     print("\nCompletely duplicated rows:")
#     print(df.duplicated().sum())


# # Load the CSV file
# df = pd.read_csv("economic_data.csv")

# # Validate the dataset
# validate_data(df)


import pandas as pd
import json


def validate_data(df):
    """Check the quality of an economic dataset."""

    problems = []

    required_columns = [
        "country",
        "GDP_growth",
        "unemployment",
        "inflation"
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        problems.append(
            f"Missing required columns: {missing_columns}"
        )
        return problems

    numeric_columns = [
    "GDP_growth",
    "unemployment",
    "inflation"
    ]

    for column in numeric_columns:
        converted = pd.to_numeric(df[column], errors="coerce")

        if converted.isna().sum() > df[column].isna().sum():
            problems.append(
            f"Non-numeric values found in {column}."
            )
    

    if df.isnull().sum().sum() > 0:
        problems.append("Missing values found.")

    if df["country"].isnull().any():
        problems.append("Missing country names found.")
    elif df["country"].str.strip().eq("").any():
        problems.append("Empty country names found.")

    unemployment_numeric = pd.to_numeric(
    df["unemployment"],
    errors="coerce"
    )

    if (unemployment_numeric < 0).any():
        problems.append("Negative unemployment values found.")
    if (unemployment_numeric > 100).any():
        problems.append("Unemployment values above 100% found.")

    if df["country"].duplicated().any():
        problems.append("Duplicate country names found.")

    if df.duplicated().any():
        problems.append("Duplicate rows found.")

    return problems

def check_unusual_values(df, inflation_limit=50, GDP_growth_limit=-10):
    """Identify unusual economic values without deleting data."""

    warnings = []

    for index, row in df.iterrows():

        country = row["country"]

        inflation = pd.to_numeric(
            row["inflation"], errors="coerce"
        )

        GDP_growth = pd.to_numeric(
            row["GDP_growth"], errors="coerce"
        )

        if inflation > inflation_limit:
            warnings.append(
                f"{country}: Inflation of {inflation}% is unusually high."
            )

        if GDP_growth < GDP_growth_limit:
            warnings.append(
                f"{country}: GDP growth of {GDP_growth}% "
                "indicates an unusually severe contraction."
            )

    return warnings

DEFAULT_CONFIG = {
    "inflation_limit": 50,
    "GDP_growth_limit": -10
}
def load_config():
    """Load configuration settings from config.json."""

    try:
        with open("config.json", "r") as file:
            config = json.load(file)

    except FileNotFoundError:
        print("Configuration file not found.")
        config = DEFAULT_CONFIG

    except json.JSONDecodeError:
        print("Invalid JSON configuration.")
        config = DEFAULT_CONFIG

    final_config = DEFAULT_CONFIG.copy()
    final_config.update(config)

    return final_config
if __name__ == "__main__":
    config = load_config()
    df = pd.read_csv("economic_data.csv")
    problems = validate_data(df)
    warnings = check_unusual_values(
    df,
    inflation_limit=config.get(
        "inflation_limit",
        DEFAULT_CONFIG["inflation_limit"]
    ),
    GDP_growth_limit=config.get(
        "GDP_growth_limit",
        DEFAULT_CONFIG["GDP_growth_limit"]
    )
)
    if problems:
        print("VALIDATION FAILED")
        for problem in problems:
            print("-", problem)
    else:
        print("VALIDATION PASSED")
        print("No problems were detected by these checks.")
        
    if warnings:
        print("\nVALIDATION WARNINGS")
        for warning in warnings:
            print("-", warning)
    else:
        print("\nNo unusual values were detected.")

