## Code to change file formats in a File View in Synapse

import synapseclient
import synapseutils
from synapseclient import Entity, Folder, File, Link, Table
import argparse
import pandas as pd

# login to synapse
syn = synapseclient.login(silent=True)

# Get arguments for table id to be changed and column to focus on
parser = argparse.ArgumentParser(
    description='Get synapse table id and columns')
parser.add_argument('table_id', type=str,
                    help='Synapse Table id for the table')
parser.add_argument('columns', nargs='+', type=str,
                    help='The column(s) to be pulled into a table query') # Will create list of column names

args = parser.parse_args()

table_id = args.table_id
columns = args.columns

# Change colum list into a string to prepare for query
column_string = ', '.join([str(column) for column in columns])

# Create query for table using specified column(s) 
table_query = (f"SELECT {column_string} FROM {table_id} "
               f"WHERE ((fileFormat = ('RAW')))")

# Create dataframe from query
file_view = syn.tableQuery(table_query).asDataFrame()
print(f"There are {len(file_view)} total results")

file_name = 'raw_file_view.xlsx'
file_view.to_excel(file_name)

# Iterate through the filenames to generate actual file formats
#file_format = []
#for filename in file_view['name'].values:
    #index = filename.index(".")
    #ext = filename[index:]
    #file_format.append(ext)

# Replace acutal file formats into the fileFormat column
#file_view['fileFormat'] = file_format

# Replace actual file formats with accepted controlled vocabulary values by creating dictionary
# drop duplicates in file_format list
#file_format = file_format = list(set(file_format))

#format_dict = {}
#for format in file_format:
   #format_dict[format] = input(f"acceptable format for {format}?")

# Replace values in data frame with accepted vocab. values based on dictionary created
#file_view = file_view.replace({'fileFormat': format_dict})
#print(file_view)

# store row changes in Synapse. Uncomment below when ready to change!
#syn.store(Table(table_id, file_view))
