import requests
import pandas as pd

url = "https://mediabiasfactcheck.com/filtered-search/?country=AU"

# Read the tables from the webpage
tables = pd.read_html(url)

# Print the number of tables found
print(f"Found {len(tables)} tables.")

# Assuming you want to convert the first table
df = tables[1]

df.sort_values('Traffic').to_csv('sources.csv')



