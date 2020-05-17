import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist, pdist
import pickle
import matplotlib.pyplot as plt
import sys
import os
from mst_clustering import MSTClustering
import seaborn as sns
sns.set()

def elbow(df, n):
	kMeansVar = [KMeans(n_clusters=k).fit(df.values) for k in range(1, n)]
	centroids = [X.cluster_centers_ for X in kMeansVar]
	k_euclid = [cdist(df.values, cent) for cent in centroids]
	dist = [np.min(ke, axis=1) for ke in k_euclid]
	wcss = [sum(d**2) for d in dist]
	tss = sum(pdist(df.values)**2)/df.values.shape[0]
	bss = tss - wcss
	plt.plot(bss)
	plt.xlabel('Clusters')
	plt.savefig('elbow.png')
	plt.clf()

if __name__=="__main__":
	#Data prep
	first=True
	for fl in [x for x in os.listdir('data') if 'ML4T' not in x and x!='Lists']:
		if first:
			df=pd.read_csv(f'data/{fl}')[['Date', 'Adj Close']].rename(columns={'Adj Close':fl.split('.')[0]})
			first=False
		else:
			df=df.merge(pd.read_csv(f'data/{fl}')[['Date', 'Adj Close']].rename(columns={'Adj Close': fl.split('.')[0]}), 'outer')
	dropcols=['SINE_SLOW_NOISE', 'SINE_FAST_NOISE', 'ABKFQ', 'CFC+A', '$VIX', 'SINE_FAST', 'SINE_SLOW','$SPX', '$DJI', 'SPY']
	df=df.drop(columns=dropcols)
	df['Date']=pd.to_datetime(df['Date'], format='%Y-%m-%d')
	df=df[df.isnull().sum(axis=1)<.1*df.shape[1]].set_index('Date').sort_values('Date')
	df/=df.shift()
	df-=1
	df=df.T
	df=df[df.isnull().sum(axis=1)<10]
	df=df.fillna(0)
	cik=pd.read_csv('cik_ticker.csv', delimiter='|')[['Ticker', 'Name', 'SIC']].dropna(subset=['SIC'])
	ind=pd.read_csv('sic_naics.csv', delimiter='|')[['SIC', 'SIC_Descrip', 'NAICS_Descrip']]
	cik['SIC']=cik['SIC'].astype(int)
	cik=cik.merge(ind, on='SIC', how='left').groupby('Ticker').first().reset_index()

	#MST Surv Ratio and Avg Link Length
	dist=[]
	tm=[]
	lnkslag=[]
	surv=[]
	for date in pd.date_range('2005-01-01', '2012-08-01', freq='MS'):
		mn,yr=(date.month, date.year)
		dis=0
		x=df[[c for c in df.columns if c.year==yr and c.month==mn]]
		mst = MSTClustering(cutoff_scale=2)
		mst.fit(x.values)
		grph=mst.get_graph_segments(full_graph=True)
		ref=[]
		for ind, row in x.iterrows():
			ref.append(list(row))
		lnks=[]
		for i in range(len(grph[0][0])):
			lnks.append([[],[]])
			for j in range(len(grph)):
				lnks[i][0].append(grph[j][0][i])
				lnks[i][1].append(grph[j][1][i])
				dis+=abs(grph[j][0][i]-grph[j][1][i])
		for i in range(len(grph[0][0])):
			lnks[i][0]=df.index[ref.index(lnks[i][0])]
			lnks[i][1]=df.index[ref.index(lnks[i][1])]
		flat=[item for sublist in lnks for item in sublist]
		full=lnks+lnkslag
		tot=len(set(tuple(i) for i in full))
		surv.append(1-((2*len(lnks)-tot)/len(lnks)))
		dist.append(dis/len(grph[0][0]))
		tm.append(pd.to_datetime(f'{yr}-{str(mn).zfill(2)}-01'))
		lnkslag=lnks

	plt.figure(figsize=(15,5))
	plt.plot(pd.date_range('2005-01-01', '2012-08-01', freq='MS')[1:],surv[1:])
	plt.ylabel('Link Survival Ratio')
	plt.savefig('surv.png')
	plt.clf()

	plt.figure(figsize=(15,5))
	plt.plot(pd.date_range('2005-01-01', '2012-08-01', freq='MS')[1:],dist[1:])
	plt.ylabel('Average Link Length')
	plt.savefig('link_l.png')
	plt.clf()

	#K-Means
	elbow(df,50)
	km=KMeans(n_clusters=30, random_state=0).fit(df.values)
	main=pd.DataFrame(data={'Ticker':list(df.index), 'Cluster':list(km.labels_)})
	main=main.merge(cik, on='Ticker', how='left')

	#Main Asset Tree
	mst = MSTClustering(cutoff_scale=2)
	mst.fit(df.values)
	grph=mst.get_graph_segments(full_graph=True)
	ref=[]
	for ind, row in df.iterrows():
		ref.append(list(row))
	lnks=[]
	for i in range(len(grph[0][0])):
		lnks.append([[],[]])
		for j in range(len(grph)):
			lnks[i][0].append(grph[j][0][i])
			lnks[i][1].append(grph[j][1][i])
	for i in range(len(grph[0][0])):
		lnks[i][0]=df.index[ref.index(lnks[i][0])]
		lnks[i][1]=df.index[ref.index(lnks[i][1])]
	flat=[item for sublist in lnks for item in sublist]
	cts=[(x, flat.count(x)) for x in set(flat)]
	cts.sort(key=lambda x: x[1], reverse = True)

	pca = PCA(n_components=2)
	trans=pca.fit_transform(df.values)
	ticks=list(df.index)
	segs=(np.zeros((2,len(lnks))),np.zeros((2,len(lnks))))
	k=0
	for lnk in lnks:
		for i in [0,1]:
			for j in [0,1]:
				segs[i][j][k]=trans[ticks.index(lnk[j])][i]
		k+=1

	main['Lab']=main['Ticker']+', '+main['NAICS_Descrip'].fillna('')
	fig, ax = plt.subplots(1, 1, figsize=(50,100), sharex=True, sharey=True)
	axi, full_graph, colors= (ax, True, km.labels_)
	axi.plot(segs[0], segs[1], '-k', zorder=1, lw=1)
	axi.scatter(trans[:, 0], trans[:, 1], c=colors, cmap='rainbow', zorder=2, s=100)
	axi.axis('tight')
	i=0
	for idx, row in main.iterrows():
		axi.annotate(row['Lab'], (trans[i,0], trans[i,1]))
		i+=1
	plt.savefig('full_tree.png')
	plt.clf()
