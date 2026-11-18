import pandas as pd

required_columns = [
    "country",
    "GDP_growth",
    "unemployment",
    "inflation"
]
def check_required_columns(df):
    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    return missing_columns

def check_duplicate_records(df, columns=None):
    duplicates = df[df.duplicated(subset=columns, keep=False)]
    total_duplicates = len(duplicates)

    return {
        "duplicates": duplicates,
        "total_duplicates": total_duplicates
    }
duplicate_df = pd.DataFrame({
    "country": ["Nigeria", "Ghana", "Nigeria"],
    "GDP_growth": [3.2, 2.8, 4.1],
    "unemployment": [4.5, 6.2, 5.0]
})
report_test_df = pd.DataFrame({
    "country": ["Nigeria", "Ghana", "Nigeria"],
    "GDP_growth": [3.2, 2.8, 4.1],
    "unemployment": [4.5, 6.2, 5.0],
    "inflation": [8.0, 7.5, 9.0]
})

duplicate_results = check_duplicate_records(duplicate_df)

print("Total duplicate records:", duplicate_results["total_duplicates"])

print("\nDuplicate records:")
print(duplicate_results["duplicates"])


data = {
    "country": ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Rwanda"],
    "GDP_growth": [3.2, None, 5.1, 1.9, 4.2, None],
    "unemployment": [4.5, 6.2, 5.0, 32.8, None, 13.0],
    "inflation": [None, 8.0, 5.1, 5.9, 12.0, None]
}

df = pd.DataFrame(data)
print(check_required_columns(df))
empty_df = pd.DataFrame()
test_df = pd.DataFrame({
    "country": ["Nigeria", "Ghana"],
    "GDP_growth": [3.2, 2.8],
    "unemployment": [4.5, 6.2]
})

print(check_required_columns(test_df))

economic_df = pd.DataFrame({
    "country": ["Nigeria", "Nigeria", "Ghana", "Ghana"],
    "year" : [2024, 2025, 2024, 2025],
    "GDP_growth" : [3.2, 4.2,2.8,2.8]
})
print("\n========== ECONOMIC DATA DUPLICATE CHECK ==========")

result = check_duplicate_records(
    economic_df,
    columns=["country", "year"]
)


print("\nEconomic DataFrame:")
print(economic_df)

print("\nDuplicate records:")
print(result["duplicates"])

print("\nTotal duplicate records:", result["total_duplicates"])

def validate_duplicates(df, columns=None):

    results = check_duplicate_records(df, columns)

    if results["total_duplicates"] > 0:
        print("Validation failed: Duplicate records found.")

    else:
        print("Validation successful: No duplicate records found.")

    return results
validation_results = validate_duplicates(
    economic_df,
    columns=["country", "year"]
)

def count_missing_values(df):
    missing_values = df.isnull().sum()
    affected_columns = missing_values[missing_values > 0]

    total_missing = missing_values.sum()
    total_countries = len(df)
    missing_rows = df[df.isnull().any(axis=1)]
    affected_countries = missing_rows["country"].tolist()
    missing_details = {}

    for index, row in missing_rows.iterrows():
        country = row["country"]
        missing_columns = row[row.isnull()].index.tolist()
        missing_details[country] = missing_columns

    return {
        "missing_values": missing_values,
        "total_missing": total_missing,
        "missing_rows": missing_rows,
        "affected_columns": affected_columns,
        "affected_countries": affected_countries,
        "missing_details": missing_details,
        "total_countries": total_countries
    }


def validate_missing_values(df):

    results = count_missing_values(df)

    if results["total_missing"] > 0:
        print("Warning: Missing values found.")
        print("Total missing values:", results["total_missing"])

    else:
        print("Validation successful: No missing values found.")

    return results

def generate_quality_report(df, duplicate_columns=None):

    if df.empty:
        raise ValueError("The uploaded dataset is empty.")

    missing_columns = check_required_columns(df)

    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    

    results = count_missing_values(df)
    duplicate_results = check_duplicate_records(df, columns=duplicate_columns)
    duplicates = duplicate_results["duplicates"]
    total_duplicates = duplicate_results["total_duplicates"]

    missing_values = results["missing_values"]
    total_missing = results["total_missing"]
    missing_rows = results["missing_rows"]
    total_cells = df.size

    completeness = round(((total_cells - total_missing) / total_cells) * 100, 2)
    incompleteness = round((total_missing / total_cells) * 100, 2)
    if completeness >= 90:
        quality_status = "Excellent"
    elif completeness >= 75:
        quality_status = "Good"
    elif completeness >= 50:
        quality_status = "Fair"
    else:
        quality_status = "Poor"
    if completeness >= 90 and total_duplicates == 0:
        overall_quality = "Excellent"
    elif completeness >= 75 and total_duplicates == 0:
        overall_quality = "Good"
    elif completeness >= 50:
        overall_quality = "Fair"
    else:
        overall_quality = "Poor"
    affected_columns = results["affected_columns"]
    affected_countries = results["affected_countries"]
    missing_details = results["missing_details"]
    total_countries = results["total_countries"]
    print("\n========== DATA QUALITY REPORT ==========")

    print("Total countries analysed:", total_countries)

    print("Total missing values:", total_missing)
    print("Total duplicate records:", total_duplicates)
    duplicate_status = "Duplicates found" if total_duplicates > 0 else "No duplicates found"
    if total_duplicates == 0:
        uniqueness_status = "Unique"
    else:
        uniqueness_status = "Duplicates detected"
    print("Duplicate status:", duplicate_status)
    print("Uniqueness status:", uniqueness_status)

    print("\nDuplicate records:")
    print(duplicates)
    print("Data completeness:", completeness, "%")
    print("Data incompleteness:", incompleteness, "%")
    print("Completeness classification:", quality_status)
    print("Overall data quality:", overall_quality)
    print("\nColumns affected by missing values:")

    for column, count in affected_columns.items():
        print(f"{column}: {count}")
    

    print("\nCountries affected by missing values:")

    for country in affected_countries:
        print(country)

    
    
    print("\nMissing data details:")

    for country, columns in missing_details.items():
        print(f"{country}: {', '.join(columns)}")
    
    return {
    "missing_values": missing_values,
    "total_missing": total_missing,
    "missing_rows": missing_rows,
    "affected_columns": affected_columns,
    "affected_countries": affected_countries,
    "missing_details": missing_details,
    "total_countries": total_countries,
    "completeness": completeness,
    "incompleteness": incompleteness,
    "quality_status": quality_status,
    "duplicates": duplicates,
    "total_duplicates": total_duplicates,
    "duplicate_status": duplicate_status,
    "uniqueness_status": uniqueness_status,
    "overall_quality": overall_quality
}

missing_results = validate_missing_values(df)


try:
    report = generate_quality_report(df, duplicate_columns=["country"])

except ValueError as error:
    print("Data validation failed:", error)

else:
    print("Data quality report generated successfully.")
    print(report["completeness"])
    print(report["quality_status"])
    print(report["duplicate_status"])
    print(report["uniqueness_status"])
    print(report["overall_quality"])

finally:
    print("Data quality checking process completed.")

