# importing pandas in order to read a CSV file from a URL because the file is too large to upload directly on to github
import pandas as pd

# URL of the CSV file
url = ("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
       "query=select+*+from+pscomppars&format=csv")

df = pd.read_csv(url)                                      # loads directly from the web into a dataframe
df.to_csv("nasa_exoplanets_raw_data.csv", index=False)     # saves the dataframe to a local CSV file

print(df.head())                                           # prints the first few rows of the dataframe

import pyvo, pandas as pd
svc = pyvo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")
res = svc.search("SELECT * FROM pscomppars", maxrec=200_000)
df  = res.to_table().to_pandas()
