import ads
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt

ads.config.token = 'QS8lYy26Fzn6x7wGkMG6onjWFttQ7UeXpb6n7hs0'

FIELDS = ['date', 'pub', 'id', 'volume', 'links_data', 'citation', 'doi',       
          'eid', 'keyword_schema', 'citation_count', 'data', 'data_facet',      
          'year', 'identifier', 'keyword_norm', 'reference', 'abstract', 'recid',
          'alternate_bibcode', 'arxiv_class', 'bibcode', 'first_author_norm',   
          'pubdate', 'reader', 'doctype', 'doctype_facet_hier', 'title', 'pub_raw', 'property',
          'author', 'email', 'orcid', 'keyword', 'author_norm',                 
          'cite_read_boost', 'database', 'classic_factor', 'ack', 'page',       
          'first_author', 'reader', 'read_count', 'indexstamp', 'issue', 'keyword_facet',
          'aff', 'facility', 'simbid']

qry = ads.SearchQuery(q='full:"lightkurve" AND year:2017-2050', rows=999999, fl=FIELDS)
papers = [q for q in qry ]

dates = [p.date for p in papers[::-1]]
titles = [p.title[0] for p in papers[::-1]]
years = [p.year for p in papers[::-1]]
authors = [p.first_author_norm for p in papers[::-1]]
bibcodes = [p.bibcode for p in papers[::-1]]
pubs = [p.pub for p in papers[::-1]]
cite_count = [p.citation_count for p in papers[::-1]]

df = pd.DataFrame({'year': years,
                   'date': pd.to_datetime(dates),
                   'title': titles,
                   'author': authors,
                   'bibcode': bibcodes,
                   'pub': pubs,
                  'cite_count': cite_count})
# Filter out Zenodo entries and AAS Abstracts
mask = ~df.pub.str.contains("(Zenodo)|(Abstracts)")
# Sort by date and reset index
df = df[mask].sort_values('date', ascending=False).reset_index(drop=True)
# Save raw stats
df.to_csv('stats.csv')

## Make a markdown table
most_recent = df.sort_values('date', ascending=False).head(5)
most_recent = most_recent.rename(columns={'date': 'Date', 'title': 'Title', 'author': 'Author'})
link_title = []
for index, row in most_recent.iterrows():
    link_title.append(f'[{row.Title}](https://ui.adsabs.harvard.edu/abs/{row.bibcode}/abstract)')
most_recent['Title'] = link_title
most_recent['Date'] = most_recent['Date'].dt.date
recent_table = most_recent[['Date', 'Title', 'Author']].to_markdown()

test = '![publications](lightkurve-publications.png) \n' + recent_table
text_file = open("readme.md", "w")
n = text_file.write(test)
text_file.close()

# Make a plot
x = pd.date_range('2018-01-01T00:00:00Z', df.date.max(), freq='1M')
y = [len(df[df.date < d]) for d in x]

fig, ax = plt.subplots(figsize=[9, 5])
plt.plot(x, y, marker='o', c='k')
plt.xlabel('Year', fontsize=12)
plt.ylabel("Publications", fontsize=12)
locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.savefig("lightkurve-publications.png")