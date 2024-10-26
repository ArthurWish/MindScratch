import pandas as pd
import semopy

# Creating a sample dataset based on the provided table
data = {
    "W1": [4, 3, 5, 4, 3, 5, 4, 3, 4, 3],
    "W2": [5, 4, 4, 4, 3, 5, 3, 4, 5, 3],
    "W3": [4, 3, 5, 4, 4, 5, 4, 3, 4, 3],
    "S1": [2, 3, 1, 2, 3, 1, 4, 3, 2, 4],
    "S2": [3, 4, 2, 2, 3, 1, 4, 3, 2, 4],
    "S3": [2, 3, 1, 2, 4, 1, 3, 4, 2, 4]
}
df = pd.DataFrame(data)

# CFA model description
model_desc = """
Wellbeing =~ W1 + W2 + W3
Stress =~ S1 + S2 + S3
"""

# Perform Confirmatory Factor Analysis
model = semopy.Model(model_desc)
result = model.fit(df)

# Displaying the results
result_summary = model.inspect()
print(result_summary)