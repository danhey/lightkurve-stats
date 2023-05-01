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
df.to_csv('stats.csv')

x = pd.date_range('2018-01-01T00:00:00Z', '2020-06-01T00:00:00Z', freq='1M')
y = [len(df[df.date < d]) for d in x]

fig, ax = plt.subplots()
plt.plot(x, y, marker='o')
plt.ylabel("Publications", fontsize=14)
locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.savefig("lightkurve-publications.pdf")