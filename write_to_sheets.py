import pygsheets
import pandas as pd



# authorization
gc = pygsheets.authorize(service_file='C:/Users/delco/Downloads/write-to-sheet-test-df1d6c34ac19.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('spike-test')

# select the first sheet
wks = sh[0]

# update the first sheet with df, starting at cell B2.
wks.set_dataframe(df, (5, 1))
