import os
import time
from sqlalchemy import create_engine, MetaData, Table
import numpy as np

import json
import random
from scipy import sparse
from scipy.sparse import issparse
from scipy.sparse import csc_matrix
from sklearn.ensemble import RandomForestClassifier

####for feature extraction
from essentiaextractor import extractFeaturesOfThese, addAllTheFiles


def readcsv(filename,feature_count,label_count):
    arr = np.loadtxt(open(filename),delimiter=",",skiprows=1)
    sparse_mat = csc_matrix(arr)
    x = sparse_mat[:,range(feature_count)]
    y = sparse_mat[:,range(feature_count,feature_count+label_count)]
    return (x.tocsr(),y.tocsr())

def get_ranking(x,y):
    rf = RandomForestClassifier(n_estimators=100, n_jobs=-1,random_state=0,criterion="entropy")
    rankings = np.zeros(shape=(6,72))
    for i in range(6):
	y_i = y[:,i].toarray()
        rf.fit(x,y_i)
        rankings[i] = rf.feature_importances_
    ranking = 0.2917369*rankings[0] + 0.2799325*rankings[1] + 0.4451939*rankings[2] + 0.2495784*rankings[3] + 0.2833052*rankings[4] + 0.3187184*rankings[5]
    return ranking

def update():
	result = os.popen("stat --format=%n:%Y songs/*").read()[:-1].split('\n')
	songs = list()
	threshold = int(time.time()) - 86400
	for song in result:
		song = song.split(':')
		if(song[1]>threshold):
			songs.append(song[0].split('/')[-1])
	
	#OMG I'm hardcoding this. Kill me now.
	# we'll read this from a file later. For now, this is faster.
	whichfeatures = [
'mean_rolloff', 
'mean_mfcc0', 
'std_mfcc11', 
'mean_mfcc1', 
'mean_centroid', 
'std_mfcc10', 
'std_mfcc8', 
'std_mfcc12', 
'std_mfcc0', 
'mean_std_centroid', 
'std_std_mfcc10', 
'std_std_mfcc11', 
'std_mfcc7', 
'std_std_mfcc1', 
'std_std_mfcc8', 
'mean_flux', 
'std_mfcc9', 
'std_std_mfcc7', 
'std_std_mfcc9', 
'std_std_mfcc6', 
'mean_std_rolloff', 
'std_std_centroid', 
'std_std_mfcc12', 
'std_std_mfcc4', 
'std_mfcc5', 
'std_mfcc4', 
'std_mfcc2', 
'std_mfcc6', 
'std_mfcc1', 
'mean_std_mfcc9', 
'mean_std_mfcc4', 
'bhsum3', 
'std_std_mfcc2', 
'std_std_mfcc3', 
'bh_lowpeakamp', 
'std_std_rolloff', 
'std_mfcc3', 
'mean_mfcc4', 
'mean_std_mfcc7', 
'bh_highpeakamp', 
'bhsum1', 
'mean_std_mfcc12', 
'mean_std_mfcc3', 
'mean_std_mfcc0', 
'std_centroid'
]
	
	#call feature extraction passing songs
	x = extractFeaturesOfThese('songs',songs,whichfeatures)

	engine = create_engine("mysql+pymysql://root:onegai123@localhost/ontag")
	metadata = MetaData(bind=engine)
	con = engine.connect()

	
	con.execute('insert into songs(name) values("'+songs[0]+'")')
	songs.pop(0)
	song_id = int(con.execute("select max(id) from songs").first()[0])
	row = np.array(np.insert(x[0],0,song_id)).ravel()
	
	con.execute("insert into features values"+str(tuple(row)))
	song_id += 1
	x = np.delete(x,0,0)

	query1 = "insert into songs(name) values "
	query2 = "insert into features values "
	for i,song in enumerate(songs):
		if i >= x.shape[0]:
			break
		query1 += '("'+song+'"),'
		row = np.array(np.insert(x[i],0,song_id)).ravel()
		query2 += str(tuple(row)) + ","
		song_id += 1

	con.execute(query1[:-1])
	con.execute(query2[:-1])

	return json.dumps(songs)
