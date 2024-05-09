import pandas, matplotlib, numpy

# import the data!
data_dataframe = pandas.read_csv('Erbium Crystals Computer Data Out.csv')
data_dataframe = data_dataframe.replace({numpy.nan: None})
plot_dataframe = all_data_dataframe.iloc[:,3:]
header = data_dataframe.columns.values[3:]
tab_width = int(len(header[3:]/2)
num_of_datapoints = data_dataframe.shape[0] - 1

fig, axes = matplotlib.subplots(tab_width,tab_width)

for row in range(0,tab_length):
    axes[row,0].set_ylabel(header[row*2])
    row_data = plot_dataframe.iloc[:, row*2]
    for col in range(row,tab_length):
        axes[0,col].setxlabel(header[col*2])
        col_data = plot_dataframe.iloc[:, col*2]
        for index in range(0,num_of_datapoints):
            if col_data[index] and 
            
        
