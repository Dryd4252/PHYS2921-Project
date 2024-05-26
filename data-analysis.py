import pandas, matplotlib.pyplot, numpy
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# import the data! convert to None! grab the data we want!
data_dataframe = pandas.read_csv('Erbium Crystals Computer Data Out.csv')
data_dataframe = data_dataframe.replace({numpy.nan: None})
plot_dataframe = data_dataframe.iloc[:,3:]

# extract some useful information, that is, the number of columns/2 (this will be the precursor to the size of the grid), the names of the columns, the amount of crystals and the names of these crystals
header = data_dataframe.columns.values[3:]
tab_width = int(len(header)/2 - 1)
num_of_datapoints = data_dataframe.shape[0] - 1
crys_names = data_dataframe.iloc[:,0]

# find correlations!
drop_indexes = list(range(1,tab_width*2 + 2,2))
drop_names = []
for i in drop_indexes:
    drop_names.append(header[i])
certain_dataframe = plot_dataframe.drop(drop_names, axis=1)

# convert to absolute value! we only have positive values! so we convert back to NaN because it plays nicer with abs!
certain_dataframe = certain_dataframe.replace({None: numpy.nan})
certain_dataframe = certain_dataframe.abs()

corr_dataframe = certain_dataframe.corr(numeric_only=False, method='pearson')
corr_dataframe.to_csv('corr_table.csv')

# we don't want to plot the refractive index!
header = list(header)

# make our grid!
fig, axes = matplotlib.pyplot.subplots(tab_width, tab_width, sharex='col', sharey='row', figsize=[30,30])

# we want the colours to be consistent with our crystals! so we choose a nice colourmap! then give each crystal a unique colour!
colour_map = matplotlib.pyplot.get_cmap('gist_rainbow')
crys_colour_dict = {}
for index in range(0, num_of_datapoints):
    crys_names[index] = crys_names[index].replace('_',"")
    crys_colour_dict[crys_names[index]] = colour_map(1.*index/num_of_datapoints)
    index = index + 1

# begin iterating over the rows of the graph-grid! assign a name to the row and also grab the row data and uncertainty! the indicies being offset is to prevent printing a variable against itself or similar!
for row in range(0, tab_width):
    axes[row,0].set_ylabel(header[row*2 + 2], fontsize=12)
    row_data, row_uncer = plot_dataframe.iloc[:, row*2 + 2], plot_dataframe.iloc[:, row*2 + 3]
    # begin iterating over the columns, do the same thing as we did before but for columns!
    for col in range(0, row + 1):
        axes[-1,col].set_xlabel(header[col*2], fontsize=12)
        col_data, col_uncer = plot_dataframe.iloc[:, col*2], plot_dataframe.iloc[:, col*2 + 1]

        # debug!
        #print("\n\n\ncurrently plotting", header[row*2 + 2], "vs", header[col*2])
        #print("with data:")
        #print(row_data)
        #print("vs:")
        #print(col_data)

        for index in range(0,num_of_datapoints):
        # plot each datapoint individually: this allows us to assign a label and name the datapoint! also a check that the data point exists so matplotlib doesn't error!
            if col_data[index] and row_data[index]:
                if col_uncer[index]:
                    xerror = abs(col_uncer[index])
                else:
                    xerror = None
                if row_uncer[index]:
                    yerror = abs(row_uncer[index])
                else:
                    yerror = None
                # determine whether to plot a o or an x depending on whether the value is computed or not!
                if col_data[index] < 0 or row_data[index] < 0:
                    axes[row,col].errorbar(abs(col_data[index]), abs(row_data[index]), xerr=xerror, yerr=yerror, capsize=1, marker='o', color=crys_colour_dict[crys_names[index]])
                elif col_data[index] > 0 and row_data[index] > 0:
                    axes[row,col].errorbar(col_data[index], row_data[index], xerr=xerror, yerr=yerror, capsize=1, marker='x', color=crys_colour_dict[crys_names[index]])
                #axes[row,col].text(col_data[index], row_data[index], crys_names[index], fontsize=8, color=crys_colour_dict[crys_names[index]])

# we create a patch for each crystal with the corresponding colour!
legend_handles = []
for crystal, colour in crys_colour_dict.items():
    legend_handles.append(Patch(facecolor=colour, label=crystal))
legend_handles.append(Line2D([0],[0],marker='x', label='Measured/From paper',color='white', markerfacecolor="black", markeredgecolor="black", markersize=10))
legend_handles.append(Line2D([0],[0],marker='o', label='Computed',color='white', markerfacecolor="black", markeredgecolor="black", markersize=10))

fig.legend(handles=legend_handles, loc='lower left')

# save the plot!
fig.savefig("many-graphs.png", format="png")
fig.savefig("many-graphs.svg", format="svg")
#matplotlib.pyplot.show()
