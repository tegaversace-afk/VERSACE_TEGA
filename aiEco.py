
# import pandas as pd

# data ={
#     'country' : ["Nigeria", "Ghana", "Kenya", "South Africa"],
#     "GDP_growth" :[3.2, 4.0, 5.1, 1.9],
#     "unemployment" : [4.5, 6.2,5.0, 32.8]
# }

# df = pd.DataFrame(data)


# print(df)

import pandas as pd

data = {
      "student_id": ["S001", "S002", "S003", "S002", "S004", "S005"],
      "name": ["  Alice ", "BOB", "Charlie", "BOB", None, "david "],
      "age": ["15", "16", "unknown", "16", "14", "17"],
      "score": [85.5, 90.0, 78.0, 90.0, None, 88.5],
      "grade": ["Grade 10", "Grade_11", "Grade 10", "Grade_11", "Grade 9", "10"],
  }
def remove_duplicates(df):
  """Removes duplicate rows based on all columns."""
  initial_count = len(df)
  df = df.drop_duplicates()
  print(f"-> Removed {initial_count - len(df)} duplicate rows.")
  return df

df = pd.DataFrame(data)

print(df)