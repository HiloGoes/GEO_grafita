import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from shapely import geometry

from geopandas import GeoDataFrame as gpd
import verde as vd
import time

grid_parameters=['MAGR','THC','KC','CTC']
plt.rcParams['figure.dpi'] = 120
dados=pd.read_csv('scrr_1039.csv')

#### Configure Geometry
dados['geometry'] = [geometry.Point(x, y) for x, y in zip(dados['UTME'], dados['UTMN'])]
crs = "+proj=utm +zone=23 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
dados = gpd(dados, geometry='geometry',crs=crs)

####  bounds
region = dados[vd.inside((dados.UTME, dados.UTMN), region= [290000, 345000,7455000, 7510000])]
coordinates = (region.UTME.values, region.UTMN.values)

def timelapse(inicio):
	timelapse=str(time.process_time()-inicio)
	print("tempo decorrido:"+timelapse+"s")

####  Chanining configuration
def chain_config(spacing=1000):
	print("chain_config begin")
	chain = vd.Chain([
		('trend',  vd.Trend(degree=2)),
		('reduce', vd.BlockReduce(np.median, spacing=spacing)),
		('spline', vd.Spline()),
		])
	print("chain_config end")
	timelapse(inicio)
	return chain

chain=chain_config()
#### Then we fit within the chain
def chaining(row=1,max_distance=1000):
	inicio=time.process_time()
	print("chaining begin")
	chain.fit(coordinates, region[row])
	grid = chain.grid(spacing=200, data_names=[row])
	grid = vd.distance_mask(coordinates, maxdist=max_distance, grid=grid)

	grid[row].to_netcdf(row+'.nc')
	grid[row].plot(figsize=(8,8), cmap='magma')
	plt.axis('scaled')
	print("chaining end")
	timelapse(inicio)
	
#### Model Validation
def validation(row,test_size=0.1,spacing=500):
	inicio=time.process_time()
	print("model validation begin")
	train, test = vd.train_test_split(coordinates, region[row], test_size=test_size, spacing=spacing)
	chain.fit(*train)
	score=chain.score(*test)
	print(score) #treino ? teste? #verde
	print("model validation end")
	timelapse(inicio)
	return score


####  Cross-Validation
def cross_validation(row):
	inicio=time.process_time()
	print("cross validation begin")
	cv = vd.BlockKFold(spacing=200,n_splits=10,shuffle=True)
	scores = vd.cross_val_score(chain,coordinates,region[row],cv=cv)
	plt.figure()
	plt.hist(scores, bins ='auto')
	print(scores)
	print("cross validation end")
	timelapse(inicio)


def process(tolerance=0.75):
	print("process begin")
	inicio=time.process_time()
	np.linspace(start=500, stop=1000, num=10)


	for row in grid_parameters:
		chaining(row)
		#if(>30%)
		validation(row)
		cross_validation(row)


	timelapse(inicio)
		#inserir flag de tempo
	
	#if error >95% continue

process()

'''
for params in other_parameters:
	np.arange(0,top+1,spacing)
'''
