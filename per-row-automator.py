import pandas, numpy, sys, os
import main
#from refractivesqlite import dboperations as refrac_DB

########## to change the db_url, change the link below! (make sure to keep the 's at the ends of the link!)
ref_db_url = 'https://refractiveindex.info/download/database/rii-database-2023-10-04.zip'
##########

# read user input! there's two possible ones!
def read_user_input(input_file='Erbium Crystals Spreadsheet.xlsx', update_refrac_db=False):
    global user_args
    user_args = {}
    user_args["input_file"] = str(input_file)
    user_args["update_refrac_db"] = bool(update_refrac_db)

try:
    read_user_input(*sys.argv[1:])
except:
    print('error: passed to many arguments to script! the script only accepts two arguments: input file and updating the refractive index db in that order!')

# import the spreadsheet into excel and convert NaN to None
all_dataframe = pandas.read_excel(user_args["input_file"])
all_dataframe = all_dataframe.replace({numpy.nan: None})

# grab only the stuff we're interested in!
dataframe_size = all_dataframe.shape
num_rows = None
num_cols = 20
properties_dataframe = all_dataframe.iloc[:num_rows, :num_cols]

# we need to pull off the inhomogenous linewidth! (and it's associated uncertainty) as david's script doesn't take those!

none_dataframe = pandas.DataFrame(data=[None]*dataframe_size[0])
inhom_dataframe = properties_dataframe.iloc[:,[11,12]]
properties_dataframe.iloc[:,[11]] = none_dataframe
properties_dataframe.iloc[:,[12]] = none_dataframe

# create empty columns for the site symmetry and normalised 
for col_name in ["Ordered Site Symmetry", "Normalised Lifetime (ms)", "Normalised Lifetime uncertainty (+-ms)"]:
    properties_dataframe = pandas.merge(properties_dataframe, none_dataframe.rename(columns={0 : col_name}), left_index=True, right_index=True)

# convert to the correct type!
to_float_cols = list(properties_dataframe.columns[3:])
to_float_cols.remove('Site Symmetry')

for column in to_float_cols:
    properties_dataframe = properties_dataframe.astype({column:'float'})
properties_dataframe = properties_dataframe.replace({numpy.nan: None})


### refractive index done manually!!!
# create a refractive index database! note that this loads the 2023 database each time! if you want to update the database, change the value near the top in a comment! note that this will load the database from this url each time (i know, it sucks, but i don't know of a better way) 

#refrac_db = refrac_DB.Database("refractive.db")
#if user_args["update_refrac_db"]:
    #refrac_db.create_database_from_url(riiurl=ref_db_url)


# do our operations per row!
for index, row in properties_dataframe.iterrows():
    
    print("processing crystal:", row[0])
    
    # refractive index done manually!!!
    # first we find the refractive index of our material!
    #refractive_index = None
    #mat_name = str(row[0]).replace('_',"")

    # we search the refractive index database!
    #search_result = refrac_db.search_custom('select * from pages where shelf="main" and book="' + mat_name + '"')
    #if search_result:
        #results_num = len(search_result) - 1
        #i = 0
        #mat = None

        # sometimes the results end up having wavelengths we don't care about.. :( so we need to catch the exceptions that happen when we try to interpolate out of the bounds using the program!
        #while i < results_num:
            #try:
                #mat = refrac_db.get_material(search_result[i][0])
                #i = i + 1
                #refractive_index = float(mat.get_refractiveindex(float(row[3])))
            #except:
                #pass
            #else:
                #if mat:
                    #break
            #finally:
                #row[17] = refractive_index
    

    # Using David's python script to compute everything, we can simply slot in a row and pull one out!
    args = row[3:]
    row_comp = main.erbium_host_crystals(*args)
    returned_vals = row_comp.get_values()
    new_row = list(row[:3]) + returned_vals
    
    properties_dataframe.iloc[index] = new_row

# yey! now hopefully nothing has gone wrong and so now we can merge our new spreadsheet with the old one! but first let's put in our inhomogenous linewidth and export the data as a CSV for convenience of my data analysis script!

# we need to do quite a few operations: this involves adding a empty dummy column for the "uncertainty" of site symmetry and removing the site symmetry column! then swapping columns!
analysis_dataframe = properties_dataframe
del analysis_dataframe['Site Symmetry']
analysis_dataframe = pandas.merge(properties_dataframe, none_dataframe, left_index=True, right_index=True)

# this is horrible, but we want to move col1 to col3, col 2 to col1, col3 to col2..
columns = list(analysis_dataframe.columns)
col1_i, col2_i, col3_i = columns.index('Ordered Site Symmetry'), columns.index('Normalised Lifetime (ms)'), columns.index('Normalised Lifetime uncertainty (+-ms)') 
columns[col1_i], columns[col3_i] = columns[col3_i], columns[col1_i]
columns[col1_i], columns[col2_i] = columns[col2_i], columns[col1_i]
analysis_dataframe = analysis_dataframe[columns]

# save!
analysis_dataframe.to_csv('Erbium Crystals Computer Data Out.csv', index=False)

# now we need to integrate this (horizontally!) so we don't lose any data!
dataframe_out = pandas.merge(properties_dataframe.iloc[:, :], all_dataframe.iloc[:, num_cols:], left_index=True, right_index=True)

# and finally export!
dataframe_out.to_excel('Erbium Crystals Spreadsheet out.xlsx', index=False)
