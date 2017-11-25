from __builtin__ import zip
from __builtin__ import map
from __builtin__ import range
from __builtin__ import str
import copy
import csv
import numpy as np
import random
from scipy import sparse
from scipy.sparse import issparse
from scipy.sparse import csc_matrix
from sqlalchemy import create_engine, MetaData, Table
import pickle
import math
import json

from sklearn.ensemble import RandomForestClassifier


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.metrics import roc_curve, auc
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

class Rakel():

    def __init__(self, classifier, model_count, labelset_size):
        self.classifier = classifier
        self.model_count = model_count
        self.labelset_size = labelset_size


    def generate_partition(self,label_count):
        label_sets = []
        self.label_count = label_count
        free_labels = range(self.label_count)

        while len(label_sets) < self.model_count:
            label_set = random.sample(free_labels, self.labelset_size)
            if label_set not in label_sets:
                label_sets.append(label_set)

        self.partition = label_sets
    
        assert len(self.partition) == self.model_count


    def predict(self, X):
        lp_predictions = [c.predict(X).tocsc() for c in self.classifiers]
        voters = [0.0]*self.label_count
        votes = sparse.csc_matrix((lp_predictions[0].shape[0], self.label_count), dtype='int')
        for model in range(self.model_count):
            for label in range(len(self.partition[model])):
                voters[self.partition[model][label]] += 1
                votes[:, self.partition[model][label]] = votes[:, self.partition[model][label]] + lp_predictions[model][:, label]

        nonzeros = votes.nonzero()
        predictions = sparse.csc_matrix((lp_predictions[0].shape[0], self.label_count), dtype='int')
        for row, column in zip(nonzeros[0], nonzeros[1]):
            if(np.round(votes[row, column] / float(voters[column]))==1):            
                predictions[row, column] = 1

        return predictions.tocsr()


    def fit(self, X, y):
        self.generate_partition(y.shape[1])
        self.classifiers = []

        for i in range(self.model_count):
            classifier = copy.deepcopy(self.classifier)
            y_subset = y.tocsc()[:, self.partition[i]]
            classifier.fit(X, y_subset)
            self.classifiers.append(classifier)

        return self

#END OF CLASS Rakel    



class LabelPowerset():

    def __init__(self, classifier):
        self.classifier = classifier
        self.clean()


    def clean(self):
        self.unique_combinations = {}
        self.reverse_combinations = []
        self.label_count = None


    def fit(self, X, y):
        self.classifier.fit(X,self.transform(y))
        return self


    def predict(self, X):
        lp_prediction = self.classifier.predict(X)
        return self.inverse_transform(lp_prediction)


    def transform(self, y):
        y = y.tolil()

        self.clean()
        self.label_count = y.shape[1]

        last_id = 0
        train_vector = []
        for labels_applied in y.rows:
            label_string = ",".join(map(str, labels_applied))

            if label_string not in self.unique_combinations:
                self.unique_combinations[label_string] = last_id
                self.reverse_combinations.append(labels_applied)
                last_id += 1

            train_vector.append(self.unique_combinations[label_string])

        return np.array(train_vector)


    def inverse_transform(self, y):
        n_samples = len(y)
        result = sparse.lil_matrix((n_samples, self.label_count), dtype='int')
        for row in range(n_samples):
            assignment = y[row]
            result[row, self.reverse_combinations[assignment]] = 1

        return result

#END OF CLASS LabelPowerset



def readcsv(filename,feature_count,label_count):
    arr = np.loadtxt(open(filename),delimiter=",",skiprows=1)
    sparse_mat = csc_matrix(arr)
    x = sparse_mat[:,range(feature_count)]
    y = sparse_mat[:,range(feature_count,feature_count+label_count)]
    return (x.tocsr(),y.tocsr())

#END OF FUNCTION readcsv


#Program Execution Begins From Here

#x_train,y_train = readcsv("emotions-train.csv",72,6)

#x_test,y_test = readcsv("emotions-test.csv",72,6)

def connect():
    engine = create_engine("mysql+pymysql://root:@localhost/ontag")
    metadata = MetaData(bind=engine)
    con = engine.connect()
    return con

def fit(songs):
    con = connect()

    user = str(songs.pop('user',))
    playlists = int(songs.pop('playlists','0'))
    song_ids = list()
    for i in songs:
        song_ids.append(int(i))
    res = con.execute("select * from features where song_id in "+str(tuple(song_ids)))
    x = np.zeros((len(songs),45))
    y = np.zeros((len(songs),playlists),dtype=int)
    i=0
    obj = {"0":[], "1":[], "2":[], "3":[], "4":[], "5":[]}
    for row in res:
        y[i] = np.asarray(songs[str(row['song_id'])]['playlists'])
        for j in range(playlists):
            if(y[i][j]==1):
                obj[str(j)].append(str(row['song_id']));
        for j in range(1,46):
            x[i][j-1] = row[j]
        i += 1
    with open("playlists","w") as datafile:
        json.dump(obj,datafile)
    count = playlists*2
    size = int(math.ceil(playlists/2))

    base_classifier = RandomForestClassifier(n_estimators=75, n_jobs=-1)
    problem_transform_classifier = LabelPowerset(classifier=base_classifier)
    classifier = Rakel(classifier=problem_transform_classifier,model_count=count,labelset_size=size)
    classifier.fit(sparse.csr_matrix(x),sparse.csr_matrix(y))
    with open("users/"+user,"w") as binfile:
        pickle.dump(classifier,binfile)
    

def predict(songs):
    con = connect()

    user = str(songs.pop('user',))
    playlists = int(songs.pop('playlists','0'))
    song_ids = list()
    for i in songs:
        song_ids.append(int(i))
    if(len(song_ids)==1):
        res = con.execute("select * from features where song_id = "+str(song_ids[0]))
    else:
        res = con.execute("select * from features where song_id in "+str(tuple(song_ids)))
    x = np.zeros((len(songs),45))
    song_ids = list()
    i=0
    for row in res:
        song_ids.append(row[0])
        for j in range(1,46):
            x[i][j-1] = row[j]
        i += 1

    with open("users/"+user) as binfile:
        classifier = pickle.load(binfile)

    pred = classifier.predict(sparse.csr_matrix(x)).toarray()

    prediction = {}

    for i in range(len(song_ids)):
        prediction[song_ids[i]] = [int(item) for item in pred[i].tolist()]

    return prediction



