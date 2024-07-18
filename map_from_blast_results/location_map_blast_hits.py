"""
This script takes the blast_results_sample.csv file rturned from bpa-otu blast search
and creates a blue marble map showing the locations of the hits returned, colored by 
their percent identity (pident) to the sequecne match.

Usage:
    python script.py <path_to_blast_results_sample.csv>

Arguments:
    path_to_blast_results_sample.csv: The path to the input file described above.
"""

import sys
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors



file_path = sys.argv[1]

# Read the blast results file, columns needed for the plot, remove duplicate lines
#file_path = 'blast_results_sample.csv'  
df = pd.read_csv(file_path, usecols=['latitude','longitude','pident'])
df_unique = df.drop_duplicates()

# Get the min and max values for lat and lon, to set the map size
min_lat, max_lat = df_unique['latitude'].min(), df_unique['latitude'].max()
min_lon, max_lon = df_unique['longitude'].min(), df_unique['longitude'].max()

# Normalize the pident values for coloring
norm = mcolors.Normalize(vmin=df_unique['pident'].min(), vmax=df_unique['pident'].max())
cmap = plt.cm.viridis

# Create the fig, axes
fig, ax = plt.subplots(figsize=(12, 8))

# Create a Basemap instance, iith bluemarble background
m = Basemap(projection='mill', llcrnrlat=min_lat-5, urcrnrlat=max_lat+5,
            llcrnrlon=min_lon-5, urcrnrlon=max_lon+5, resolution='c')

m.bluemarble()

# Plot each point point with color based on pident value
x, y = m(df_unique['longitude'].values, df_unique['latitude'].values)
sc = m.scatter(x, y, c=df_unique['pident'].values, cmap=cmap, norm=norm, marker='o', zorder=5)

# colorbar and titles
cbar = m.colorbar(sc, location='right', pad='5%')
cbar.set_label('pident')
plt.title('Locations of related sequences')

# Save it
plt.savefig('blast_hit_location_map.png', dpi=300, bbox_inches='tight')

plt.show()