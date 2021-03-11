

import numpy as np#
import pandas as pd
import matplotlib.pyplot as plt

import pyproj#
from shapely import geometry

from geopandas import GeoDataFrame as gpd
import verde as vd
import rasterio as rio

grid_parameters=['MAGR','THC','UC','KC','CTC']
plt.rcParams['figure.dpi'] = 120

dados=pd.read_csv('scrr_1039.csv')

#### Configure Geometry
dados['geometry'] = [geometry.Point(x, y) for x, y in zip(dados['UTME'], dados['UTMN'])]
crs = "+proj=utm +zone=23 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
dados = gpd(dados, geometry='geometry',crs=crs)

####  bounds
region = dados[vd.inside((dados.UTME, dados.UTMN), region= [290000, 345000,7455000, 7510000])]
coordinates = (region.UTME.values, region.UTMN.values)

####  Chanining configuration
chain = vd.Chain([
	('trend',  vd.Trend(degree=2)),
	('reduce', vd.BlockReduce(np.median, spacing=1000)),
	('spline', vd.Spline()),
	])

"""shake region configuration"""
def shake_region():#don't implemnt with other variables changes (after model is valuable)
	return 0
#### Then we fit within the chain
def chaining(row,max_distance=1000):
	chain.fit(coordinates, region[row])
	grid = chain.grid(spacing=200, data_names=[row])
	grid = vd.distance_mask(coordinates, maxdist=max_distance, grid=grid)
	pass

	grid[row].plot(figsize=(8,8), cmap='magma')
	plt.axis('scaled')
	
#### Model Validation
def validation(row,test_size=0.1,spacing=500):
	train, test = vd.train_test_split(coordinates, region[row], test_size=test_size, spacing=spacing)
	chain.fit(*train)
	chain.score(*test)
	pass

####  Cross-Validation
def cross_validation(row):
	cv = vd.BlockKFold(spacing=200,n_splits=10,shuffle=True)
	scores = vd.cross_val_score(chain,coordinates,region[row],cv=cv)
	plt.figure()
	plt.hist(scores, bins ='auto')
	scores
'''
for row in grid_parameters:
	chaining(row)
	validation(row)
	other(row)
	#if error <95% continue

for params in other_parameters:
	np.arange(0,top+1,spacing)
	

'''