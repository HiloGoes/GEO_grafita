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
dados = dados[vd.inside((dados.UTME, dados.UTMN), region=[290000, 345000,7455000, 7510000])]
coordinates = (dados.UTME.values, dados.UTMN.values)




### Counter
def timelapse(begin,str_process="@@"):
	timelapse=np.floor(process_time()-begin) #transform to int
	Min_timelapse="00"#configuring as default value
	if timelapse>=60:
		Min_timelapse=timelapse/60
		timelapse=timelapse%60
		print(str_process+" timelapse: "+str(Min_timelapse)+":"+str(timelapse))

####  Chanining configuration
def chain_config(spacing=2500,degree=7):#degree>20 is useless ##operations with 2 degree polynomium can go downwards or upwards very fast
    begin=process_time()
    print("chain_config begin")
    chain = vd.Chain([
		('trend',  vd.Trend(degree=degree)),
		('reduce', vd.BlockReduce(np.median, spacing=spacing)),
		('spline', vd.Spline()),
		])
    timelapse(begin,"chain_config")
    return chain

def fitting():#for each feature
	begin=process_time()
	print(feature+' chain fit begin')
	chain.fit(coordinates, dados[feature])
	timelapse(begin,"chain fit")

#### Plot grid
def griding(max_distance=500,cell_size=500):
	begin=process_time()
	print(feature+'chaining begin')
	grid = chain.grid(spacing=cell_size, data_names=[feature])
	grid = vd.distance_mask(coordinates, maxdist=max_distance, grid=grid)
	grid[feature].to_netcdf('~/graphite_git/resources/tif/verde/'+feature+'_'+max_distance+'_'+cell_size+'.nc')
	grid[feature].plot(figsize=(8,8), cmap='magma')
	plt.axis('scaled')
	timelapse(begin,"griding")
	return grid
	
	

#### Model Validation
def validation(sample_block_size = 500,test_size=0.1):
	begin=process_time()
	print("model validation begin")
	train, test = vd.train_test_split(coordinates, dados[feature], test_size=test_size, spacing=sample_block_size)
	chain.fit(*train)
	score=chain.score(*test)
	print(score)
	timelapse(begin,"model validation")
	return score


####  Cross-Validation
def cross_validation():
	begin=process_time()
	print("cross validation begin")
	cv = vd.BlockKFold(spacing=100,n_splits=10,shuffle=True)
	scores = vd.cross_val_score(chain,coordinates,dados[feature],cv=cv)
	plt.figure()
	plt.hist(scores, bins ='auto')
	print("cross validation end")
	timelapse(begin)
	return scores

#pop from
def throw_chaining(spacing):
	begin=process_time()
	print("@@@throw_chaining_process begin")
	for x in spacing:
		fitting()
		if validation(feature)<success_rate:
			print("	...throwing chaining")
		else:
			print("good result!")
			chain=chain_config(x)
			grid[feature].to_netcdf(feature+str(process_time())+'.nc')#just check-it for tests
			break
	timelapse(begin,"@@@end throw_chaining")
	return chain


### GLOBALS
feature='@@'
chain=chain_config() #computacional throw effort, at check human default values
success_rate=0.75
grid_results={}

print("##process begin")
begin=process_time()
spacing=np.linspace(start=500, stop=1000, num=10)[::-1]

for params in grid_parameters:
	feature=params
	throw_chaining(spacing)
	validation(params)
	cross_validation(params)
	grid_results[feature]=griding()
	break
timelapse(begin,"##end process")