#! python3
import pandas as pd

url = "https://mediabiasfactcheck.com/filtered-search/?country=AU"

# Read the tables from the webpage
tables = pd.read_html(url)

# Print the number of tables found
print(f"Found {len(tables)} tables.")

# Assuming you want to convert the first table
df = tables[1]

df = df.sort_values(
    by=['Traffic', 'Popularity Estimate'],
    ascending=[True, False]
).set_index('News Source')


df['Track'] = None


## Investigate https://discover.abc.net.au/#/?query=energy%20OR%20nuclear&sortBy=ABC_production_all_latest
df.loc['ABC News Australia','Track'] = [
        'https://www.abc.net.au/news/topic/electricity-production-and-distribution',
        'https://www.abc.net.au/news/topic/energy-research',
        'https://www.abc.net.au/news/topic/nuclear-energy',
        'https://www.abc.net.au/news/topic/alternative-energy',
        'https://www.abc.net.au/news/topic/biofuel',
        'https://www.abc.net.au/news/topic/electrical-products-industry',
        'https://www.abc.net.au/news/topic/energy-industry',
        'https://www.abc.net.au/news/topic/energy-policy',
        'https://www.abc.net.au/news/topic/energy-research',
        'https://www.abc.net.au/news/topic/geothermal-energy',
        'https://www.abc.net.au/news/topic/greenhouse-gases',
        'https://www.abc.net.au/news/topic/hydro-energy',
        'https://www.abc.net.au/news/topic/hydrogen-fuel',
        'https://www.abc.net.au/news/topic/mining-environmental-issues',
        'https://www.abc.net.au/news/topic/mining-and-metals-industry',
        'https://www.abc.net.au/news/topic/nuclear-issues',
        'https://www.abc.net.au/news/topic/solar-energy',
        'https://www.abc.net.au/news/topic/climate-change',
        'https://www.abc.net.au/news/topic/utilities',
        'https://www.abc.net.au/news/topic/wind-energy',
     ]

df.loc['News.com.au','Track'] = ['https://www.news.com.au/search-results?q=Energy']



