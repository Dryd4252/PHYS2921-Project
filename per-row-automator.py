import pandas, numpy, sys, os
import main 
from refractivesqlite import dboperations as refrac_DB

########## to change the db_url, change the link below! (make sure to keep the 's at the ends of the link!)
ref_db_url = 'https://refractiveindex.info/download/database/rii-database-2023-10-04.zip'
##########

# import the spreadsheet into excel and convert NaN to None

sys_args = sys.argv
if len(sys_args) < 2:
    file_to_read = 'Erbium Crystals Spreadsheet.xlsx'
else:
    file_to_read = sys_args[1]

all_dataframe = pandas.read_excel(file_to_read)
all_dataframe = all_dataframe.replace({numpy.nan: None})

# grab only the stuff we're interested in!
#num_rows = 20
num_rows = None
num_cols = 19
properties_dataframe = all_dataframe.iloc[:num_rows, :num_cols]

# convert to the correct type!
for column in list(properties_dataframe.columns)[3:]:
    properties_dataframe = properties_dataframe.astype({column:'float'})
properties_dataframe = properties_dataframe.replace({numpy.nan: None})

# create a refractive index database! note that this loads the 2023 database each time! if you want to update the database, change the value near the top in a comment! note that this will load the database from this url each time (i know, it sucks, but i don't know of a better way)

refrac_db = refrac_DB.Database("refractive.db")
# refrac_db.create_database_from_url(riiurl=ref_db_url)



# do our operations per row!
for index, row in properties_dataframe.iterrows():

    # first we find the refractive index of our material!
    refractive_index = None
    mat_name = str(row[0]).replace('_',"")

    # we search the refractive index database!
    search_result = refrac_db.search_custom('select * from pages where shelf="main" and book="' + mat_name + '"')
    if search_result:
        results_num = len(search_result) - 1
        i = 0
        mat = None

        # sometimes the results end up having wavelengths we don't care about.. :( so we need to catch the exceptions that happen when we try to interpolate out of the bounds using the program!
        while i < results_num:
            try:
                mat = refrac_db.get_material(search_result[i][0])
                i = i + 1
                refractive_index = float(mat.get_refractiveindex(float(row[3])))
            except:
                pass
            else:
                if mat:
                    break
            finally:
                row[17] = refractive_index
    # Using Daniel's python script to compute everything, we can simply slot in a row and pull one out!
    args = row[3:]
    row_comp = main.erbium_host_crystals(*args)
    returned_vals = row_comp.get_values()
    new_row = list(row[:3]) + returned_vals
    
    properties_dataframe.iloc[index] = new_row

# yey! now hopefully nothing has gone wrong and so now we can merge our new spreadsheet with the old one! but first let's export the data as a CSV for convenience of my data analysis script!
open('Erbium Crystals Computer Data Out.csv', 'w').close()
properties_dataframe.to_csv('Erbium Crystals Computer Data Out.csv', index=False)

# now we need to integrate this (horizontally and then vertically!) to combine with our spreadsheet!
dataframe_out = pandas.merge(properties_dataframe.iloc[0:, 0:], all_dataframe.iloc[0:, num_cols:], left_index=True, right_index=True)
dataframe_out = pandas.concat([dataframe_out, all_dataframe.iloc[num_rows:, 0:]])

# and finally export!
open('Erbium Crystals Spreadsheet out.xlsx', 'w').close()
dataframe_out.to_excel('Erbium Crystals Spreadsheet out.xlsx', index=False)
