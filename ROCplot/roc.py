from builtins import zip
from builtins import map
from builtins import range
from builtins import str
import copy
import csv
import numpy as np
import random
from scipy import sparse
from scipy.sparse import issparse
from scipy.sparse import csc_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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
        lp_predictions = [
            c.predict(X).tocsc()
            for c in self.classifiers
        ]
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
    
    def predict_proba(self, X):
        lp_predictions = [
            c.predict_proba(X).tocsc()
            for c in self.classifiers
        ]
	voters = [0.0]*self.label_count
        votes = sparse.csc_matrix((lp_predictions[0].shape[0], self.label_count), dtype='float')
        for model in range(self.model_count):
            for label in range(len(self.partition[model])):
		voters[self.partition[model][label]] += 1
                votes[:, self.partition[model][label]] = votes[:, self.partition[model][label]] + lp_predictions[model][:, label]

        nonzeros = votes.nonzero()
	predictions = sparse.csc_matrix((lp_predictions[0].shape[0], self.label_count), dtype='float')
        for row, column in zip(nonzeros[0], nonzeros[1]):
            predictions[row, column] = votes[row, column] / float(voters[column])

        return predictions.toarray()
    
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
    
    def predict_proba(self, X):
        lp_prediction = self.classifier.predict_proba(X)
        result = sparse.lil_matrix(
            (X.shape[0], self.label_count), dtype='float')
        for row in range(len(lp_prediction)):
            assignment = lp_prediction[row]
            for combination_id in range(len(assignment)):
                for label in self.reverse_combinations[combination_id]:
                    result[row, label] += assignment[combination_id]        
	return result
    
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


#Function To Measure The Performance of the Classifier

def performance(y,predictions):
    y = y.tolil()
    predictions = predictions.tolil()
    y_rows = y.rows
    predictions_rows = predictions.rows
    CA = 0
    P = 0.0
    R = 0.0
    A = 0.0
    match = 0
    
    for y_row,predictions_row in zip(y_rows,predictions_rows):
        if(y_row == predictions_row):
            CA += 1;
        match = 0
        for y_ele in y_row:
            if(y_ele in predictions_row):
                match += 1;
        if(predictions_row):
            P += match/float(len(predictions_row))
            R += match/float(len(y_row))
            A += match/float(len(predictions_row)+len(y_row)-match)
                                    
    global classification_accuracy
    global precision
    global recall
    global accuracy

    classification_accuracy = CA/float(y.shape[0])
    precision = P/y.shape[0]
    recall = R/y.shape[0]
    accuracy = A/y.shape[0]

#END OF FUNCTION performance


#Function To Read a CSV File as a CSR Sparse Matrix

def readcsv(filename,feature_count,label_count):
    arr = np.loadtxt(open(filename),delimiter=",",skiprows=1)
    sparse_mat = csc_matrix(arr)
    x = sparse_mat[:,range(feature_count)]
    y = sparse_mat[:,range(feature_count,feature_count+label_count)]
    return (x.tocsr(),y.tocsr())

#END OF FUNCTION readcsv

#Function For feature Ranking
def get_ranking(x,y):
    rf = RandomForestClassifier(n_estimators=100, n_jobs=-1,random_state=0,criterion="entropy")
    rankings = np.zeros(shape=(6,72))
    for i in range(6):
	y_i = y[:,i].toarray()
        rf.fit(x,y_i)
        rankings[i] = rf.feature_importances_
    ranking = 0.2917369*rankings[0] + 0.2799325*rankings[1] + 0.4451939*rankings[2] + 0.2495784*rankings[3] + 0.2833052*rankings[4] + 0.3187184*rankings[5]
    return ranking
        
#END OF FUNCTION get_ranking

#Program Execution Begins From Here

classification_accuracy = 0.0
precision = 0.0
recall = 0.0
accuracy = 0.0

ca = 0.0
p = 0.0
r = 0.0
a = 0.0

x,y = readcsv("dataset.csv",72,6)

ranking = dict(zip(range(72),get_ranking(x,y)))
rank = sorted(ranking, key=lambda x : ranking[x],reverse=True)

x_train1,x_test1,y_train,y_test = train_test_split(x,y,test_size=0.2)


#1
x_test = x_test1[:,rank[0:45]]
x_train = x_train1[:,rank[0:45]]
base_classifier = RandomForestClassifier(n_estimators=75, n_jobs=-1)
problem_transform_classifier = LabelPowerset(classifier=base_classifier)
classifier = Rakel(classifier=problem_transform_classifier,model_count=12,labelset_size=3)
classifier.fit(x_train,y_train)
predictions = classifier.predict(x_test)
pred = classifier.predict_proba(x_test)
performance(y_test,predictions)
ca += classification_accuracy
p += precision
r += recall
a += accuracy
# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(6):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i].toarray(), pred[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.toarray().ravel(), pred.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# Compute macro-average ROC curve and ROC area

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(6)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(6):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= 6

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         color='deeppink', linestyle=':', linewidth=4)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)

colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
for i, color in zip(range(6), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=i,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=i)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Some extension of Receiver operating characteristic to multi-class')
plt.legend(loc="lower right")
plt.savefig("RF75.png")
   

#print str(i+1) + "Classification accuracy is " + str(ca)
print str(i+1) + "Precision is " + str(p)
print str(i+1) + "Recall is " + str(r)
#print str(i+1) + "Accuracy is " + str(a)


#END