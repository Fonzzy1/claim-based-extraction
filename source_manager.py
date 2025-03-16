#! python3
import pandas as pd
import requests as r

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

df.to_csv('sources.csv')


df['Text'] = None
df['Audio'] = None
df['Video'] = None

df.at['ABC News Australia', 'Audio'] = ['https://www.abc.net.au/listen/radionational/transcripts']
df.at['ABC News Australia', 'Text'] = [
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
        'https://www.abc.net.au/news/topic/wind-energy'
    ]
df.at['ABC News Australia', 'Video'] = [  
         'https://www.youtube.com/@abcnewsaustralia/videos',  
         'https://www.tiktok.com/@abcnewsaus'  
     ]  

df.at['News.com.au','Video'] =['https://www.youtube.com/@newscomauhq/videos','https://www.tiktok.com/@news.com.au?lang=en']
# the text and audio is a bit mixed together for news.com
# will need to sort out a good parse
df.at['News.com.au','Text'] =['https://www.news.com.au/search-results?q=Energy']
df.at['News.com.au','Audio'] =['https://www.youtube.com/@newscomauhq/videos']


df.at['The Sydney Morning Herald', 'Text'] = ['https://www.smh.com.au/search?text=+Energy&page=10']
# The morning edition sits inside the YouTube channel; just need to pull them
# out sensibly.
df.at['The Sydney Morning Herald', 'Video'] = ['https://www.youtube.com/@smhtheage/videos']
df.at['The Sydney Morning Herald', 'Audio'] = ['https://www.youtube.com/@smhtheage/videos']

df.at['The Conversation', 'Text'] = ['https://www.smh.com.au/search?text=+Energy&page=10']
df.at['The Conversation', 'Video'] = ['https://www.tiktok.com/@theconversation.aunz']
df.at['The Conversation', 'Audio'] = [
    "https://theconversation.com/au/podcasts/politics-with-michelle-grattan",
    "https://theconversation.com/au/podcasts/below-the-line",
    "https://theconversation.com/au/podcasts/mediafiles",
    "https://theconversation.com/au/podcasts/trust-me-podcast",
    "https://theconversation.com/au/podcasts/Essays-On-Air",
    "https://theconversation.com/au/podcasts/speaking-with",
    "https://theconversation.com/au/podcasts/business-briefing",
    "https://theconversation.com/au/podcasts/change-agents",
    "https://theconversation.com/au/podcasts/us-election-podcast"
]

df.at['The Daily Telegraph (AUS)', 'Text'] = ['https://www.dailytelegraph.com.au/search-results']
df.at['The Daily Telegraph (AUS)', 'Video'] = ['https://www.youtube.com/@dailytelegraphAU', 'https://www.tiktok.com/@dailytelegraph?lang=en']
df.at['The Daily Telegraph (AUS)', 'Audio'] = ['https://www.dailytelegraph.com.au/search-results?q=Daily%20Telegraph%20%E2%80%93%20News%20Feed']

df.at['The Australian', 'Text'] = ['https://www.theaustralian.com.au/search-results']
df.at['The Australian', 'Video'] = ['https://www.youtube.com/@theaustralian/videos', 'https://www.tiktok.com/@the.australian?lang=en']
df.at['The Australian', 'Audio'] = ['https://www.youtube.com/playlist?list=PLfDC8EeZJyt1IVjv5bCRbFBkTl-VYpJyf']

# The Australian Financial Review
df.at['The Australian Financial Review', 'Text'] = ['https://www.afr.com/search/articles?text=Energy']
# No audio presence
df.at['The Australian Financial Review', 'Audio'] = ['https://www.youtube.com/@FinancialReview/videos']

# ScienceAlert
df.at['ScienceAlert', 'Text'] = ['https://www.sciencealert.com/search?q=Energy']
df.at['ScienceAlert', 'Video'] = ['https://www.youtube.com/@sciencealert/videos']

# 9 News (Australia)
df.at['9 News (Australia)', 'Text'] = ['https://www.9news.com.au/energy/1']
df.at['9 News (Australia)', 'Video'] = ['https://www.youtube.com/@9NewsAUS/videos']
# has a range of radio networks, but I'm struggling to find my content

# The Age (Australia)
df.at['The Age (Australia)', 'Text'] = ['https://www.theage.com.au/topic/energy-5wp?page=10']
# Note this is the same as the smh stuff
df.at['The Age (Australia)', 'Video'] = ['https://www.youtube.com/@smhtheage/videos']
df.at['The Age (Australia)', 'Audio'] = ['https://www.youtube.com/@smhtheage/videos']

# Herald-Sun (Australia)
df.at['Herald-Sun (Australia)', 'Text'] = ['https://www.heraldsun.com.au/topics/future-energy']
df.at['Herald-Sun (Australia)', 'Video'] = ['https://www.tiktok.com/@heraldsun_?lang=en','https://www.youtube.com/@heraldsun/videos']
df.at['Herald-Sun (Australia)', 'Audio'] = ['https://www.heraldsun.com.au/search-results']

# Special Broadcasting Service
# All of them are in the same feed
df.at['Special Broadcasting Service', 'Text'] = ['https://www.sbs.com.au/news/collection/energy']
df.at['Special Broadcasting Service', 'Video'] = ['https://www.sbs.com.au/news/collection/energy']
df.at['Special Broadcasting Service', 'Audio'] = ['https://www.sbs.com.au/news/collection/energy']

# 7NEWS
df.at['7NEWS', 'Text'] = ['https://7news.com.au/business/energy']
df.at['7NEWS', 'Video'] = ['https://www.youtube.com/@7news/videos','https://www.tiktok.com/@7newsaustralia?lang=en']
# No clear podcasts

# Sky News Australia
df.at['Sky News Australia', 'Text'] = ['https://www.skynews.com.au/business/energy/page/1']
df.at['Sky News Australia', 'Video'] = ['https://www.youtube.com/@SkyNewsAustralia/videos']
## No clear podcasts, lot of overlap with video content


# The New Daily
df.at['The New Daily', 'Text'] = ['https://www.thenewdaily.com.au/tag/energy?page=1']


pivot_df = df.reset_index()[['News Source', 'Text', 'Audio', 'Video']]

# Pivot the table so media types become columns
pivot_table = pivot_df.melt(id_vars=['News Source'],
                            var_name='MediaType', 
                            value_name='Source')

exploded_table = pivot_table.explode('Source')

exploded_table=exploded_table.loc[exploded_table['Source'].apply(bool)]

exploded_table.reset_index(drop=True).to_csv('source_urls.csv')

